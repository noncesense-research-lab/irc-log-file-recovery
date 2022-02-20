"""
IRC spelunking

Recovering images from several Noncesense Research Lab projects that were posted to public logged IRC channels

Mitchell Krawiec-Thayer (@Isthmus), 2022-02
"""

# Import libraries
import isthmuslib  # == 0.0.56
from isthmuslib import pd, tqdm, time, pathlib  # (standard libraries)
import requests

# Specify paths
data_path: pathlib.Path = pathlib.Path.cwd() / 'data' / 'version_controlled' / 'mrl_freenode.txt'
output_directory: pathlib.Path = pathlib.Path.cwd() / 'data' / 'version_controlled' / 'recovered_files'

# Read in the logs and extract the URLs with `isthmuslib.extract_text_to_dataframe()`
with open(data_path, 'r') as f:
    text: str = f.read()
df: pd.DataFrame = isthmuslib.extract_text_to_dataframe(input_string=text, record_delimiter='] <',
                                    tokens_dictionary={'raw': ((left := 'https://usercontent.irccloud-cdn.com'), '\n')})

# Download the files
for url in tqdm(left + df['raw']):
    r: requests.models.Response = requests.get(str(url), allow_redirects=True)
    open(f"{output_directory / (str(time.time()).split('.')[0])}_{url.split('/')[-1]}", 'wb').write(r.content)
    time.sleep(3)
