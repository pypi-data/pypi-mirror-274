from pysma.definitions_speedwire import commands

class Test_speedwire_class:
    """Test the Speedwire class."""

    async def test_unique_responses(self):
        response = set()
        duplicates = set()
        for r in commands.values():
          #  print(r)
            resp = f'{r["response"]:X}'
            if  resp in response:
                duplicates.add(resp)
            else:
                response.add(resp)
        print(duplicates)
        assert len(duplicates) == 0


    # async def test_unique_command(self):
    #     cmds = set()
    #     duplicates = set()
    #     for r in commands.values():
    #       #  print(r)
    #         resp = f'{r["command"]:X}'
    #         if  resp in cmds:
    #             duplicates.add(resp)
    #         else:
    #             cmds.add(resp)
    #     print(duplicates)
    #     assert len(duplicates) == 0
