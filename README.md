# UniFrame Developer Examples
This repository shows you how to use Python scripts to communicate with uniframe.io and do string matching.

## Prerequisite to run the examples
1. Sign-up a user on [uniframe.io](https://uniframe.io).
2. Create a `.env` file in the root path of this repository, and fill by the following content. Please replace the email and password by your actual ones.
```sh
USERNAME=<YOUR_EMAIL>
PASSWORD=<YOUR-PASSWORD>
```
3. Install Python package `requests`, `pandas` and `dotenv`.
```
pip install -r requriements.txt
```

## Run examples
You can run the python files in the `examples` directly
```
python examples/<EXAMPLE-FILE>.py
```

## Examples
- [login_get_bearer_token.py](./examples/login_get_bearer_token.py): login with the registered username and password, and get bearer token for API. Read this [page](https://www.devopsschool.com/blog/what-is-bearer-token-and-how-it-works/) for more information about bearer token.
- [create_dataset.py](./examples/create_dataset.py): create a dataset by using the dummy dataset [demo-gt.csv](./assets/data/demo-gt.csv) and [demo-matching.csv](./assets/data/demo-matching.csv)
- [create_batch_task.py](./examples/create_batch_task.py): create a batch string matching task.
- [run_batch_task.py](./examples/run_batch_task.py): run a batch string matching task.
- [create_rt_task.py](./examples/create_rt_task.py): create a real-time string matching task.
- [launch_rt_task.py](./examples/launch_rt_task.py): launch a real-time string matching task.
- [rt_searching.py](./examples/rt_searching.py): do real-time string matching search.
- [delete_dataset_and_task.py](./examples/delete_dataset_and_task.py): delete all datasets and tasks you created. When you create datasetf or tasks, if you get error message like "Name has been used", you can change a dataset or task name, or use this script to clear all the datasets and tasks.

## More information
- Please visit our [documentation](https://doc.uniframe.io/) if you want to know what is string matching and other terminology.
- Please visit our [Swagger API document](https://api.uniframe.io/docs). **N.B. in order to visit our Swagger API document, you need to first login [uniframe.io](uniframe.io)**
- If you have more questions, please contact info@uniframe.io
