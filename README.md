# MarketSummaryAI
![Demo](https://github.com/Joseph-M-Cook/MarketSummaryAI/blob/9fc2fd65c3c61964212771858b6cf2e044df8b34/MarketSummaryDEMO.jpg)

## Overview
MarketSummaryAI is a tool that leverages the power of OpenAI's GPT-4 to provide brief summaries of daily stock market activities. It uses Selenium for web scraping to fetch heatmaps from the cryptocurrency market and the S&P 500, allowing users to get a visual sense of the market's performance.

To keep users informed, the application summarizes the key points from CNBC's 'Five Things to Know' for a quick and comprehensive market update. These summaries are generated using OpenAI's GPT-4, a state-of-the-art language model capable of understanding and generating human-like text based on given inputs.

Furthermore, MarketSummaryAI integrates with the GroupMe messaging platform, enabling it to automatically send the fetched heatmaps and the generated market summaries directly to a GroupMe chat. This way, users can stay updated on the go without needing to visit multiple sites or platforms.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Joseph-M-Cook/MarketSummaryAI.git
```
2. Install the required dependencies:

```bash 
pip install -r requirements.txt
```
3. Set up API keys and private IDs. You need to provide your own API keys for both GroupMe and OpenAI.
   - `BOT_ID`
   - `ACCESS_TOKEN`
   - `OPEN_AI_API_KEY`

4. Set the script to execute locally on a program like Window's Task Scheduler


## Disclaimer
Please use this responsibly and ensure you comply with both OpenAI's and GroupMe's terms of service.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
