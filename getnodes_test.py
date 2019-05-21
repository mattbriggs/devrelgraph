import getnodes as GN
import devrelutilities as DR

TESTREPO = "testdata\\"
TESTBLACKLIST = ["index"]

def test_create_nodes():
    testlist = GN.create_nodes(TESTREPO, TESTBLACKLIST)
    result = [['path', 'type', 'filename'], ['\\file1.md', 'article', 'file1'], ['\\file2.md', 'article', 'file2'], ['\\file3.md', 'article', 'file3']]

    assert testlist == result