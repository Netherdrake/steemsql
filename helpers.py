from steemtools.blockchain import Blockchain
from tqdm import tqdm


def scrape_with_progress(start_block, end_block, filter_by):
    b = Blockchain()
    events = []
    with tqdm(total=end_block - start_block) as progress_bar:
        last_block_id = start_block
        for event in b.replay(start_block=start_block, end_block=end_block, filter_by=filter_by):
            events.append(event)

            current_block = int(event['block_id'])
            if current_block != last_block_id:
                progress_bar.update(current_block - last_block_id)
                last_block_id = current_block

    return events
