import pytest

from emailaddressvalidator import EmailAddressValidator

def test_email_only():
    assert not EmailAddressValidator()('joe.banana@example.com')

def test_email_only_missing_user():
    with pytest.raises(AssertionError):
         assert EmailAddressValidator()('@example.com')

def test_email_only_missing_at():
    with pytest.raises(AssertionError):
         assert EmailAddressValidator()('joe.banana.example.com')

def test_email_and_name():
    '''
    Fun fact: This validator does *not* understand the form with name and email.
    '''
    with pytest.raises(AssertionError):
        assert EmailAddressValidator()('Joe Banana <joe.banana@example.com>')
