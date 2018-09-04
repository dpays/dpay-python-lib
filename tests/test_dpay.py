import unittest

from dpaypy.post import Post
from dpaypy.dpay import DPay
from dpaypy.exceptions import (
    MissingKeyError,
    InsufficientAuthorityError,
    VotingInvalidOnArchivedPost
)

identifier = "@jared/dpaypy"
testaccount = "jared"
wif = {
    "active": "5KkUHuJEFhN1RCS3GLV7UMeQ5P1k5Vu31jRgivJei8dBtAcXYMV",
    "posting": "5KkUHuJEFhN1RCS3GLV7UMeQ5P1k5Vu31jRgivJei8dBtAcXYMV",
    "owner": "5KkUHuJEFhN1RCS3GLV7UMeQ5P1k5Vu31jRgivJei8dBtAcXYMV"
}
dpay = DPay(nobroadcast=True, keys=wif)


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Testcases, self).__init__(*args, **kwargs)
        self.post = Post(identifier, dpay_instance=dpay)

    def test_getOpeningPost(self):
        self.post._getOpeningPost()

    def test_reply(self):
        try:
            self.post.reply(body="foobar", title="", author=testaccount, meta=None)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_upvote(self):
        try:
            self.post.upvote(voter=testaccount)
        except VotingInvalidOnArchivedPost:
            pass
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_downvote(self, weight=-100, voter=testaccount):
        try:
            self.post.downvote(voter=testaccount)
        except VotingInvalidOnArchivedPost:
            pass
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_edit(self):
        try:
            dpay.edit(identifier, "Foobar")
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_post(self):
        try:
            dpay.post("title", "body", meta={"foo": "bar"}, author=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_create_account(self):
        try:
            dpay.create_account("jared-create",
                                 creator=testaccount,
                                 password="foobar foo bar hello world",
                                 storekeys=False
                                 )
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_transfer(self):
        try:
            dpay.transfer("jared", 10, "BEX", account=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_withdraw_vesting(self):
        try:
            dpay.withdraw_vesting(10, account=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_transfer_to_vesting(self):
        try:
            dpay.transfer_to_vesting(10, to=testaccount, account=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_get_replies(self):
        dpay.get_replies(author=testaccount)

    def test_get_posts(self):
        dpay.get_posts()

    def test_get_balances(self):
        dpay.get_balances(testaccount)

    def test_getPost(self):
        self.assertEqual(Post("@jared/dpaypy", dpay_instance=dpay).url,
                         "/dpaypy/@jared/dpaypy")
        self.assertEqual(Post({"author": "@jared", "permlink": "dpaypy"}, dpay_instance=dpay).url,
                         "/dpaypy/@jared/dpaypy")


if __name__ == '__main__':
    unittest.main()
