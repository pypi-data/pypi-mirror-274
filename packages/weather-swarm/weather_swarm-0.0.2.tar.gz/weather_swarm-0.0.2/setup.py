# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weather_swarm']

package_data = \
{'': ['*']}

install_requires = \
['json', 'pydantic==2.7.1', 'swarms==4.9.9', 'transformers']

setup_kwargs = {
    'name': 'weather-swarm',
    'version': '0.0.2',
    'description': 'Weather Swarm - Pytorch',
    'long_description': "# Baron Weather\n\n## Overview\nBaron Weather is a sophisticated toolset designed to enable real-time querying of weather data using the Baron API. It utilizes a swarm of autonomous agents to handle concurrent data requests, optimizing for efficiency and accuracy in weather data retrieval and analysis.\n\n## Features\nBaron Weather includes the following key features:\n- **Real-time Weather Data Access**: Instantly fetch and analyze weather conditions using the Baron API.\n- **Autonomous Agents**: A swarm system for handling multiple concurrent API queries efficiently.\n- **Data Visualization**: Tools for visualizing complex meteorological data for easier interpretation.\n\n## Prerequisites\nBefore you begin, ensure you have met the following requirements:\n- Python 3.9 or newer\n- git installed on your machine\n\n## Installation\n\n### Cloning the Repository\nTo get started with Baron Weather, clone the repository to your local machine using:\n\n```bash\ngit clone https://github.com/baronservices/weatherman_agent.git\ncd weatherman_agent\n```\n\n### Setting Up the Environment\nCreate a Python virtual environment to manage dependencies:\n\n```bash\npython -m venv venv\nsource venv/bin/activate  # On Windows use `venv\\Scripts\\activate`\n```\n\n### Installing Dependencies\nInstall the necessary Python packages via pip:\n\n```bash\npip install -r requirements.txt\n```\n\n## Usage\nTo start querying the Baron Weather API using the autonomous agents, run:\n\n```bash\npython main.py\n```\n\n## Contributing\nContributions to Baron Weather are welcome and appreciated. Here's how you can contribute:\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/YourAmazingFeature`)\n3. Commit your Changes (`git commit -m 'Add some YourAmazingFeature'`)\n4. Push to the Branch (`git push origin feature/YourAmazingFeature`)\n5. Open a Pull Request\n\n## License\nBaron Weather is released under the MIT License. See the `LICENSE` file for more details.\n\n## Contact\nProject Maintainer - [Kye Gomez](mailto:kye@swarms.world) - [GitHub Profile](https://github.com/baronservices)\n\n## Acknowledgements\n- Thanks to the Baron API for providing access to their weather data services.\n- Thanks to all contributors who help maintain and enhance this project.\n\n\n# Todo\n- Make API server functional\n- Make Dockerfile\n- Create a team of specialized agents for different types of weather tools.",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/baronservices/weatherman_agent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
