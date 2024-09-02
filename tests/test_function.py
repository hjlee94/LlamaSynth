
def import_test():
    try:
        import llama_synth
    except:
        return -1
    
    return 0

def test():
    assert import_test() >= 0

