import random


def random_profession(track, params, **kwargs):
    # choose a suitable index: if there is only one defined for this track
    # choose that one, but let the user always override index and type.
    if len(track.indices) == 1:
        default_index = track.indices[0].name
        if len(track.indices[0].types) == 1:
            default_type = track.indices[0].types[0].name
        else:
            default_type = None
    else:
        default_index = "_all"
        default_type = None

    index_name = params.get("index", default_index)
    type_name = params.get("type", default_type)

    # you must provide all parameters that the runner expects
    versions = params["versions"]
    lowerI = random.randint(0, len(versions) - 1)
    lower = versions[lowerI]
    upper = versions[random.randint(lowerI, len(versions) - 1)]
    print("lower %s : upper %s" % (lower,upper))

    return {
        "body": {
            "query": {
                "range": {
                    "my_version": {
                        "gte" : "%s" % lower,
                        "lte" : "%s" % upper
                    }
                }
            }
        },
        "index": index_name,
        "type": type_name,
        "cache": params.get("cache", False)
    }

def register(registry):
    registry.register_param_source("my-custom-term-param-source", random_profession)
