class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def oddEvenList(head):
    # write code here
    odd = True
    cur = head
    head2 = ListNode(-1)
    cur2 = head2
    last = None
    final = None
    while cur:
        print(cur.val)
        if odd:
            if not cur.next or not cur.next.next:
                final = cur
            last = cur
            cur = cur.next
            odd = False
        else:
            print('last', last.val)
            last.next = cur.next
            cur2.next = cur
            cur2 = cur2.next
            temp = cur
            cur = cur.next
            temp.next = None
            odd = True
    final.next = head2.next
    print(final.val)
    return head

head = ListNode(2)
head2 = ListNode(3)
head3 = ListNode(4)
head4 = ListNode(5)
head5 = ListNode(6)
head.next = head2
head2.next = head3
head3.next = head4
head4.next = head5
ret = oddEvenList(head)
print( )
print(ret.val)
print(ret.next.val)
print(ret.next.next.next.val)
