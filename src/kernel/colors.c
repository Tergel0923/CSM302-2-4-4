// SPDX-License-Identifier: GPL-2.0
/* Part I: intrusive circular doubly linked list with a small proc interface. */
#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/list.h>
#include <linux/mutex.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/uaccess.h>
#include <linux/capability.h>
#include <linux/string.h>

struct color { unsigned int id; int red, green, blue; struct list_head list; };
static LIST_HEAD(color_list);
static DEFINE_MUTEX(lock);
static unsigned int count, next_id = 1, found;
static struct proc_dir_entry *entry;
#define LIMIT 128

static void clear_list(void)
{
    struct color *p, *tmp;
    list_for_each_entry_safe(p, tmp, &color_list, list) {
        list_del(&p->list);
        kfree(p);
    }
    count = 0; found = 0;
}
static int add_color(int r, int g, int b)
{
    struct color *p;
    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255)
        return -EINVAL;
    if (count >= LIMIT || next_id == 0) return -ENOSPC;
    p = kmalloc(sizeof(*p), GFP_KERNEL);
    if (!p) return -ENOMEM;
    p->id = next_id++; p->red = r; p->green = g; p->blue = b;
    INIT_LIST_HEAD(&p->list);
    list_add_tail(&p->list, &color_list);
    count++;
    return 0;
}
/* Construct replacement first: allocation failure leaves the old list intact. */
static int reset_list(void)
{
    LIST_HEAD(fresh);
    struct color *p, *tmp;
    int i;
    const int rgb[4][3] = {{138,226,43},{255,0,0},{0,255,0},{0,0,255}};
    for (i = 0; i < 4; i++) {
        p = kmalloc(sizeof(*p), GFP_KERNEL);
        if (!p) {
            list_for_each_entry_safe(p, tmp, &fresh, list) {
                list_del(&p->list); kfree(p);
            }
            return -ENOMEM;
        }
        p->id = i + 1; p->red = rgb[i][0]; p->green = rgb[i][1]; p->blue = rgb[i][2];
        INIT_LIST_HEAD(&p->list); list_add_tail(&p->list, &fresh);
    }
    clear_list(); list_splice_tail_init(&fresh, &color_list);
    count = 4; next_id = 5;
    return 0;
}
static unsigned int node_id(struct list_head *link)
{
    return link == &color_list ? 0 : list_entry(link, struct color, list)->id;
}
static int show(struct seq_file *m, void *v)
{
    struct color *p;
    mutex_lock(&lock);
    seq_printf(m, "{\"kind\":\"colors\",\"found\":%u,\"head\":{\"next\":%u,\"prev\":%u},\"nodes\":[", found,
               node_id(color_list.next), node_id(color_list.prev));
    list_for_each_entry(p, &color_list, list) {
        seq_printf(m, "%s{\"id\":%u,\"r\":%d,\"g\":%d,\"b\":%d,\"next\":%u,\"prev\":%u}",
                   p->list.prev == &color_list ? "" : ",", p->id, p->red, p->green, p->blue,
                   node_id(p->list.next), node_id(p->list.prev));
    }
    seq_puts(m, "]}\n");
    mutex_unlock(&lock);
    return 0;
}
static int open_file(struct inode *inode, struct file *file) { return single_open(file, show, NULL); }
static ssize_t write_file(struct file *file, const char __user *buf, size_t len, loff_t *off)
{
    char text[96], *cursor, *token, *args[5];
    int argc = 0;
    int r, g, b, ret = -EINVAL;
    unsigned int id;
    struct color *p;
    if (!capable(CAP_SYS_ADMIN)) return -EPERM;
    if (!len || len >= sizeof(text)) return -EINVAL;
    if (copy_from_user(text, buf, len)) return -EFAULT;
    /* Reject embedded NUL, preventing hidden trailing commands. */
    if (memchr(text, '\0', len)) return -EINVAL;
    text[len] = '\0';
    cursor = strim(text);
    while ((token = strsep(&cursor, " \t\r\n")) != NULL) {
        if (!*token) continue;
        if (argc == ARRAY_SIZE(args)) return -EINVAL;
        args[argc++] = token;
    }
    if (!argc) return -EINVAL;
    mutex_lock(&lock);
    if (argc == 4 && (!strcmp(args[0], "ADD") || !strcmp(args[0], "SEARCH"))) {
        if (kstrtoint(args[1], 10, &r) || kstrtoint(args[2], 10, &g) ||
            kstrtoint(args[3], 10, &b) || r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255)
            goto done;
        if (!strcmp(args[0], "ADD")) {
            ret = add_color(r, g, b); if (!ret) found = 0;
        } else {
            found = 0; ret = 0;
            list_for_each_entry(p, &color_list, list)
                if (p->red == r && p->green == g && p->blue == b) { found = p->id; break; }
        }
    } else if (argc == 2 && !strcmp(args[0], "DELETE")) {
        if (kstrtouint(args[1], 10, &id)) goto done;
        ret = -ENOENT;
        list_for_each_entry(p, &color_list, list) {
            if (p->id == id) { list_del(&p->list); kfree(p); count--; found = 0; ret = 0; break; }
        }
    } else if (argc == 1 && !strcmp(args[0], "RESET")) ret = reset_list();
    else if (argc == 1 && !strcmp(args[0], "CLEAR")) { clear_list(); ret = 0; }
done:
    mutex_unlock(&lock);
    return ret ? ret : len;
}
static const struct proc_ops ops = { .proc_open = open_file, .proc_read = seq_read,
    .proc_lseek = seq_lseek, .proc_release = single_release, .proc_write = write_file };
static int __init colors_init(void)
{
    struct color *p;
    int ret = reset_list();
    if (ret) return ret;
    entry = proc_create("kds_colors", 0600, NULL, &ops);
    if (!entry) { clear_list(); return -ENOMEM; }
    list_for_each_entry(p, &color_list, list)
        pr_info("kds_colors: id=%u RGB=(%d,%d,%d)\n", p->id, p->red, p->green, p->blue);
    return 0;
}
static void __exit colors_exit(void)
{
    unsigned int freed;
    proc_remove(entry);
    mutex_lock(&lock); freed = count; clear_list(); mutex_unlock(&lock);
    pr_info("kds_colors: removed %u nodes; list empty=%d\n", freed, list_empty(&color_list));
}
module_init(colors_init); module_exit(colors_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("II-4-4 color linked list and graph interface");
