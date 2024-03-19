class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


last = ListNode(1, None)
middle = ListNode(0, last)
first = ListNode(1, middle)


def getDecimalValue(head: ListNode) -> int:
    ans = 0

    s = 0

    while head:

        if head.val == 0:
            s += 1
            head = head.next
            continue
        else:
            ans += 2 ** s
        s += 1
        head = head.next

    return ans


print(getDecimalValue(first))