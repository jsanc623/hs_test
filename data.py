from operator import itemgetter

TIME_CUTOFF = 600000


def transform(dataset):
    if len(dataset) == 0 or "events" not in dataset:
        return None

    # create our output data object
    output = {"sessionsByUser": {}}

    # sort our full dataset by timestamp
    events = sorted(dataset["events"], key=itemgetter('timestamp'))

    previous = {}
    for event in events:
        if event["visitorId"] not in output["sessionsByUser"]:
            output["sessionsByUser"][event["visitorId"]] = [{
                "duration": 0,
                "pages": [],
                "startTime": event["timestamp"]
            }]
            previous[event["visitorId"]] = event
            previous[event["visitorId"]]["idx"] = 0

        # get our last index
        idx = previous[event["visitorId"]]["idx"]

        # calculate our time differences
        gtt, difference = time_gt_cutoff(event["timestamp"], previous[event["visitorId"]]["timestamp"])

        if not gtt:
            output["sessionsByUser"][event["visitorId"]][idx]["duration"] += difference
            output["sessionsByUser"][event["visitorId"]][idx]["pages"].append(event["url"])
        else:
            output["sessionsByUser"][event["visitorId"]].append({
                "duration": 0,
                "pages": [event["url"]],
                "startTime": event["timestamp"]
            })

        # keep track of our previously seen event by visitorId
        previous[event["visitorId"]] = event

        # keep track of our list index
        previous[event["visitorId"]]["idx"] = len(output["sessionsByUser"][event["visitorId"]]) - 1

    return output


def time_gt_cutoff(time_a, time_b):
    """ returns true if time difference is greater than TIME_CUTOFF as well as the difference """
    return abs(time_a - time_b) > TIME_CUTOFF, abs(time_a - time_b)
