
"""Manipulate an LED in a dedicated thread, fed by a command queue.
    Code originally retrieved as a part of 
"""

import threading
import Queue


try:
    from digihw import user_led_set
except:
    import time
    def user_led_set(value, led):
        print "%15f: LED %d -- %d" % (time.time(), led, value)


class LEDHandler(threading.Thread):
    """An LED handler thread managed via an input queue."""

    def __init__(self, led, inqueue):
	"""Create an LED handler thread for a specific LED, with a command queue."""

        self.inqueue = inqueue
        self.curr_led = led        # LED to manage
        self.next_value = False    # initially off, not enforced
        self.action_list = [self.block]

        self.reset_state()

        threading.Thread.__init__(self)

    def run(self):
	"""Run main loop for LED handler, including parsing command queue input."""

        while True:
            newstr = None
            try:
                newstr = self.inqueue.get(True,self.curr_timeout)
            except Queue.Empty:
                pass

            if newstr is not None:
            	if newstr == "quit":
            	    return
                self.parse_str(newstr)

            # Take next action, assume action should take no time
            self.curr_timeout = 0
            self.action_list[self.next_entry]()
            # The curr_timeout and next_entry may have been modified
            self.next_entry = self.next_entry + 1

    def reset_state(self):
        self.multiplier = 1000.0   # Default to milliseconds
        self.curr_timeout = 0      # 0 indicates we should simply move on
        self.next_entry = 0        # Next element to process
        self.loop_target = -1      # a 'c'ontinue will loop to beginning
        
    def block(self):
        self.next_entry = self.next_entry - 1  # backup to repeat this one
        self.curr_timeout = 3600.0  # wait an hour, at least

    def update_multiplier(self, f):
        self.multiplier = f

    def set_state(self, value):
        self.next_value = value
        user_led_set(self.next_value, self.curr_led)

    def delay_and_toggle(self, duration):
        user_led_set(self.next_value, self.curr_led)
        secs = duration / self.multiplier
        self.curr_timeout = secs
        self.next_value = not self.next_value    # toggle

    def set_loop_target(self, idx):
        self.loop_target=idx

    def close_loop(self):
        self.next_entry = self.loop_target

    def parse_str(self,s):
        tokens=s.split(',')
    
        self.action_list=[]
        for t,idx in zip(tokens,xrange(len(tokens))):
            if t == "on":
                self.action_list.append(lambda: self.set_state(value=True))

            elif t == "off":
                self.action_list.append(lambda: self.set_state(value=False))

            elif t == "s":
                self.action_list.append(lambda: self.update_multiplier(1.0))

            elif t == "ms":
                self.action_list.append(lambda: self.update_multiplier(1000.0))

            elif t == "ns":
                self.action_list.append(lambda: self.update_multiplier(1000000.0))

            elif t == "l":
                self.action_list.append(lambda idx=idx: self.set_loop_target(idx))
    
            elif t == "c":
                self.action_list.append(self.close_loop)
    
            else:
                try:
                    i=int(t)
                    self.action_list.append(lambda i=i: self.delay_and_toggle(i))
                except:
                    print "Unexpected token! (",t,")"
                    raise ValueError

        self.action_list.append(self.block)
        self.reset_state()


if __name__ == '__main__':
    import time
    q = Queue.Queue()
    print "Setting up a simple test on LED 1"
    h = LEDHandler(1, q)
    h.start()

    print "Starting a heartbeat on LED 1"
    print '  ms,on,l,250,100,200,450,c'
    q.put("ms,on,l,250,100,200,450,c")

    print "... for 10 seconds... "
    time.sleep(10)

    print "Now a simple 0.25 HZ blink"
    print '  s,on,l,2,c'
    q.put("s,on,l,2,c")

    print "... for 15 seconds... "
    time.sleep(15)

    print "Now a fast blink"
    print '  ms,on,l,10,c'
    q.put("ms,on,l,10,c")

    print "... for 5 seconds... "
    time.sleep(5)

    print "Finally, a pause, 4 winks, and off"
    print '  "s,off,4," + "2,1,"*4 + "off"'
    q.put("s,off,4," + "2,1,"*4 + "off")

    time.sleep(20)  # allow previous script to complete
    q.put("quit")   # kill handling thread
