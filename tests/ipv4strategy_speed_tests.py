#!/usr/bin/env python
"""
A little script to prove the speed difference between a basic AddrStrategy
support IPv6 and a customised subclass of AddrStrategy that implements certain
methods using Python socket and struct modules.

Sample output on my beastly 3GHz Intel Core 2 Quad Q9450!

5000 iterations, repeated 3 time(s)

AddrStrategy timings:
--------------------
[0.21094412837385756, 0.2100993282665814, 0.20949589961852699]
avg: 0.21017978542

IPv4Strategy timings:
--------------------
[0.060295512418477748, 0.059709544090100874, 0.059620566301024303]
avg: 0.0598752076032

IPv4Strategy is 3.5x faster than AddrStrategy!
"""

import os
import sys
import pprint
from timeit import Timer

#   Run all unit tests for all modules.
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from netaddr.strategy import *

ST_IPV4_BASIC = AddrStrategy(addr_type=AT_INET, width=32, word_size=8,
                         word_fmt='%d', word_sep='.', word_base=10)

#-----------------------------------------------------------------------------
print 'Bargain basement strategy setup :-'
print '-'*80
pprint.pprint(ST_IPV4_BASIC.__dict__)
print '-'*80

#-----------------------------------------------------------------------------
def ipv4_opt_speed_test():
    ST_IPV4.str_to_int('192.168.0.1')
    ST_IPV4.int_to_str(3232235521)
    ST_IPV4.int_to_words(3232235521)
    ST_IPV4.words_to_int((192, 168, 0, 1))

#-----------------------------------------------------------------------------
def ipv4_std_speed_test():
    ST_IPV4_BASIC.str_to_int('192.168.0.1')
    ST_IPV4_BASIC.int_to_str(3232235521)
    ST_IPV4_BASIC.int_to_words(3232235521)
    ST_IPV4_BASIC.words_to_int((192, 168, 0, 1))

#-----------------------------------------------------------------------------
def ipv4_speed_test():
    repeat = 3
    iterations = 5000
    t1 = Timer('ipv4_std_speed_test()',
               'from __main__ import ipv4_std_speed_test')
    results1 = t1.repeat(repeat, iterations)
    avg1 = sum(results1) / float(len(results1))

    t2 = Timer('ipv4_opt_speed_test()',
               'from __main__ import ipv4_opt_speed_test')
    results2 = t2.repeat(repeat, iterations)
    avg2 = sum(results2) / float(len(results2))

    print '%r iterations, repeated %r time(s)' % (iterations, repeat)
    print 'AddrStrategy timings:', results1, 'avg:', avg1
    print 'IPv4Strategy timings:', results2, 'avg:', avg2
    print 'IPv4Strategy is %.1fx faster than AddrStrategy!' \
        % (avg1 / avg2)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    ipv4_speed_test()