// SPDX-License-Identifier: GPL-2.0
#include <linux/module.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/list.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include "collatz_math.h"
struct number { unsigned int id; unsigned long long value; struct list_head list; };
static LIST_HEAD(sequence);
static unsigned long long start = 25;
module_param(start, ullong, 0);
MODULE_PARM_DESC(start, "Positive initial value, default 25");
static struct proc_dir_entry *entry;
static unsigned int count;
#define MAX_NODES 4096
static void clear_sequence(void)
{
    struct number *p, *tmp;
    list_for_each_entry_safe(p, tmp, &sequence, list) { list_del(&p->list); kfree(p); }
    count = 0;
}
static unsigned int node_id(struct list_head *p)
{ return p == &sequence ? 0 : list_entry(p, struct number, list)->id; }
static int show(struct seq_file *m, void *v)
{
    struct number *p;
    seq_printf(m, "{\"kind\":\"collatz\",\"start\":\"%llu\",\"head\":{\"next\":%u,\"prev\":%u},\"nodes\":[",
               start, node_id(sequence.next), node_id(sequence.prev));
    list_for_each_entry(p, &sequence, list)
        seq_printf(m, "%s{\"id\":%u,\"value\":\"%llu\",\"next\":%u,\"prev\":%u}",
                   p->id == 1 ? "" : ",", p->id, p->value, node_id(p->list.next), node_id(p->list.prev));
    seq_puts(m, "]}\n"); return 0;
}
static int open_file(struct inode *inode, struct file *file) { return single_open(file, show, NULL); }
static const struct proc_ops ops = { .proc_open = open_file, .proc_read = seq_read,
    .proc_lseek = seq_lseek, .proc_release = single_release };
static int __init collatz_init(void)
{
    unsigned long long n = start, next;
    struct number *p;
    int ret;
    if (!n) return -EINVAL;
    for (;;) {
        if (count >= MAX_NODES) { ret = -E2BIG; goto fail; }
        p = kmalloc(sizeof(*p), GFP_KERNEL);
        if (!p) { ret = -ENOMEM; goto fail; }
        p->id = ++count; p->value = n;
        INIT_LIST_HEAD(&p->list); list_add_tail(&p->list, &sequence);
        if (n == 1) break;
        if (kds_next(n, &next)) { ret = -ERANGE; goto fail; }
        n = next;
    }
    entry = proc_create("kds_collatz", 0400, NULL, &ops);
    if (!entry) { ret = -ENOMEM; goto fail; }
    list_for_each_entry(p, &sequence, list)
        pr_info("kds_collatz: node=%u value=%llu\n", p->id, p->value);
    return 0;
fail:
    clear_sequence(); pr_err("kds_collatz: generation failed (%d), allocation rolled back\n", ret); return ret;
}
static void __exit collatz_exit(void)
{
    unsigned int freed = count;
    proc_remove(entry); clear_sequence();
    pr_info("kds_collatz: removed %u nodes; list empty=%d\n", freed, list_empty(&sequence));
}
module_init(collatz_init); module_exit(collatz_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("II-4-4 parameterized Collatz kernel linked list");
