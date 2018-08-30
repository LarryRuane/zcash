#!/usr/bin/env python2
# Copyright (c) 2018 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, start_nodes, wait_and_assert_operationid_status

from decimal import Decimal

# Test wallet z_listunspent and z_listreceivedbyaddress behaviour across network upgrades
# TODO: Test z_listreceivedbyaddress
class WalletListNotes(BitcoinTestFramework):

    def setup_nodes(self):
        return start_nodes(4, self.options.tmpdir, [[
            '-nuparams=5ba81b19:202', # Overwinter
            '-nuparams=76b809bb:204', # Sapling
        ]] * 4)

    def run_test(self):
        # Current height = 200 -> Sprout
        print self.nodes[0].getblockcount()
        assert_equal(200, self.nodes[0].getblockcount())
        sproutzaddr = self.nodes[0].z_getnewaddress('sprout')
        saplingzaddr = self.nodes[0].z_getnewaddress('sapling')
        print "sprout zaddr", sproutzaddr
        print "saplingzaddr", saplingzaddr
        assert_equal(0, Decimal(self.nodes[0].z_gettotalbalance()['private']))
        
        # Set current height to 201 -> Sprout
        self.nodes[0].generate(1)
        self.sync_all()
        assert_equal(201, self.nodes[0].getblockcount())

        mining_addr = self.nodes[0].listunspent()[0]['address']
        # Shield coinbase funds
        recipients = [{"address":sproutzaddr, "amount":Decimal('10.0')-Decimal('0.0001')}] # utxo amount less fee
        myopid = self.nodes[0].z_sendmany(mining_addr, recipients)
        txid_1 = wait_and_assert_operationid_status(self.nodes[0], myopid)
        self.sync_all()
        
        # No funds (with one or more confirmations) in sproutzaddr yet
        assert(not self.nodes[0].z_listunspent())
        
        # no private balance because no confirmations yet
        print "type", type(self.nodes[0].z_gettotalbalance()['private'])
        assert_equal(0, Decimal(self.nodes[0].z_gettotalbalance()['private']))
        
        # list private unspent, this time allowing 0 confirmations
        unspent_cb = self.nodes[0].z_listunspent(0)
        assert_equal(1, len(unspent_cb))
        assert_equal(False,                             unspent_cb[0]['change'])
        assert_equal(txid_1,                            unspent_cb[0]['txid'])
        assert_equal(True,                              unspent_cb[0]['spendable'])
        assert_equal(sproutzaddr,                       unspent_cb[0]['address'])
        assert_equal(Decimal('10.0')-Decimal('0.0001'), unspent_cb[0]['amount'])

        # list unspent, filtering by address, should produce same result
        unspent_cb_filter = self.nodes[0].z_listunspent(0, 9999, False, [sproutzaddr])
        assert_equal(unspent_cb, unspent_cb_filter)
        
        # Generate a block to confirm shield coinbase tx
        self.nodes[0].generate(1)
        self.sync_all()
        assert_equal(202, self.nodes[0].getblockcount())
        
        # Current height = 202 -> Overwinter. Default address type remains Sprout
        sproutzaddr2 = self.nodes[0].z_getnewaddress()
        assert_equal('sprout', self.nodes[0].z_validateaddress(sproutzaddr2)['type'])
        recipients = [{"address": sproutzaddr2, "amount":Decimal('1.0')-Decimal('0.0001')}]
        myopid = self.nodes[0].z_sendmany(sproutzaddr, recipients)
        txid_2 = wait_and_assert_operationid_status(self.nodes[0], myopid)
        self.sync_all()
        
        # list unspent, allowing 0conf txs
        unspent_tx = self.nodes[0].z_listunspent(0)
        print "unspent_tx1:", unspent_tx
        unspent_tx_filter = self.nodes[0].z_listunspent(0, 9999, False, [sproutzaddr2])
        assert_equal(len(unspent_tx), 2)
        unspent_tx = sorted(unspent_tx, key=lambda k: k['amount'])
        print "unspent_tx2:", unspent_tx
        assert_equal(False,                             unspent_tx[0]['change'])
        assert_equal(txid_2,                            unspent_tx[0]['txid'])
        assert_equal(True,                              unspent_tx[0]['spendable'])
        assert_equal(sproutzaddr2,                      unspent_tx[0]['address'])
        assert_equal(Decimal('1.0')-Decimal('0.0001'),  unspent_tx[0]['amount'])

        assert_equal(True,                              unspent_tx[1]['change'])
        assert_equal(txid_2,                            unspent_tx[1]['txid'])
        assert_equal(True,                              unspent_tx[1]['spendable'])
        assert_equal(sproutzaddr,                       unspent_tx[1]['address'])
        assert_equal(Decimal('9.0')-Decimal('0.0001'),  unspent_tx[1]['amount'])
        # TODO: test change
        
        # No funds in saplingzaddr yet
        assert(not self.nodes[0].z_listunspent(0, 9999, False, [saplingzaddr]))
        
        # Current height = 204 -> Sapling
        # self.nodes[0].generate(2)

if __name__ == '__main__':
    WalletListNotes().main()
