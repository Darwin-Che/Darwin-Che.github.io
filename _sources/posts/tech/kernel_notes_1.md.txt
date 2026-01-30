# Notes derived from reading the Understanding Linux Kernel book

During interrupt handler, because there's no process context,
sleep is not possible for both upper half and bottom half (softirq and tasklet).
Therefore, spinlock is the only mechanism.
The book describe that spinlock is not reentrant, an execution thread can
deadlock itself if not careful.
The book points out therefore using spinlock itself is often not enough
by itself. Things can go wrong if hardware interrupt happens when the spinlock
is held. The interrupt handler might need the spinlock to insert to a queue
for example, and thus deadlock. So whenever using a spinlock, consider if this
spinlock is used in the any interrupt context, if so, disable interrupt to
avoid deadlock. The kernel provides a shortcut called `spin_lock_irqsave`
and `spin_unlock_irqrestore`.

It was also mentioned that bottom halfs can actually preempt process execution.
So `spin_lock_bh` sometimes is needed.

---

On Page 215, there are `time_after` and `time_before` macros to resolve
jiffies overflow and wrap. 
I still don't quite understand how those macro solve the issue.

