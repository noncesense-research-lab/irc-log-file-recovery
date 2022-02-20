"""
IRC spelunking

Recovering images from several Noncesense Research Lab projecs that were posted to IRC back in 2019ish and not backed up elsewhere

Mitchell Krawiec-Thayer (@Isthmus), 2022-02
"""

# Import libraries
import isthmuslib
from isthmuslib import pd, tqdm, time, pathlib, Dict, List, Tuple, Any  # (standard libraries)
import requests

# Specify paths
data_path: pathlib.Path = pathlib.Path.cwd() / 'data' / 'version_controlled' / 'mrl_freenode.txt'
output_directory: pathlib.Path = pathlib.Path.cwd() / 'data' / 'version_controlled' / 'recovered_files'

# Read in the data
with open(data_path, 'r') as f:
    text: str = f.read()
df: pd.DataFrame = isthmuslib.extract_text_to_dataframe(input_string=text, record_delimiter='] <',
                                    tokens_dictionary={'raw': ((left := 'https://usercontent.irccloud-cdn.com'), '\n')})
df['url'] = left + df['raw']

# Download the files
for url in tqdm(left + df['raw']):
    print(f"\nDownloading: {(last_part := url.split('/')[-1])}")
    r: requests.models.Response = requests.get(str(url), allow_redirects=True)
    open(f"{output_directory / (str(time.time()).split('.')[0])}_{last_part}", 'wb').write(r.content)
    time.sleep(3)
