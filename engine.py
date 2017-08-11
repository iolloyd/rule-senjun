import lib.redis_conn

def labels():
    pass


def matches():
    pass


def engine():
    pass


def rules():
    """Fetch rules from source.
    Rules have the following structure:
        [
          {
           'label': 'skinny:jeans', 
           'match': ['crop:top', 'fluffy:top', 'opentop:shoes', 'kinky:boots']
          },
          {
           'label': 'red:shirt',
           'match': ['boyfriend:jeans', 'red:skirt']
          }
        ]
    """
    matching_rules = get_rules()
    matching_rules = process_rules(matching_rules)
    return matching_rules


def find_matching_outfits(ids):
    """ids -> [[ids]]"""

    labels = [labels_for_id(id) for id in ids]
     

