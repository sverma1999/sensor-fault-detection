from src.kafka_producer.json_producer import produce_data_using_file
from src.constant import SAMPLE_DIR
import os

if __name__ == "__main__":
    """This is the main function from where the execution starts of the producer"""

    # Step 1: Get the list of topic name and sample data file path=================================

    # Sample data is stored in the following directory,
    # listdir() returns a list containing the names of the entries in the directory given by path.
    topics = os.listdir(SAMPLE_DIR)

    # Remove .DS_Store from the list if there is any
    if ".DS_Store" in topics:
        topics.remove(".DS_Store")
    print(f"topics: [{topics}]")

    # For each topic, we will get the sample file path and produce the data using that file
    for topic in topics:
        # os.path.join() method in Python join one or more path components intelligently.
        sample_topic_data_dir = os.path.join(SAMPLE_DIR, topic)

        sample_file_path = os.path.join(
            sample_topic_data_dir, os.listdir(sample_topic_data_dir)[0]
        )
        produce_data_using_file(topic=topic, file_path=sample_file_path)
