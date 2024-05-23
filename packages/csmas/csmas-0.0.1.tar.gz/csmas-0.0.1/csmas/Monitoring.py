import sys
import psutil
import platform
from datetime import datetime, timezone
import cpuinfo
import yaml
import asyncio
import requests


cpu_name = cpuinfo.get_cpu_info()['brand_raw']

def get_size(bytes, suffix="B"):
	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor

def get_sys_info():
	uname = platform.uname()
	boot_time_timestamp = psutil.boot_time()
	bt = datetime.fromtimestamp(boot_time_timestamp)
	up_time = datetime.now() - bt
	up_time = str(up_time).split('.')[0]
	cpufreq = psutil.cpu_freq()
	svmem = psutil.virtual_memory()
	swap = psutil.swap_memory()
	partitions = psutil.disk_partitions()
	total = []
	used = []
	perc = []
	for partition in partitions:
		try:
			partition_usage = psutil.disk_usage(partition.mountpoint)
			total.append(partition_usage.total)
			used.append(partition_usage.used)
			perc.append(partition_usage.percent)
		except PermissionError:
			continue
	total_num = sum(total)
	used_num = sum(used)
	perc_num = sum(perc) / len(perc)
	net_io = psutil.net_io_counters()
	disk_io = psutil.disk_io_counters()
	info = f"""```yaml
{"="*20} System {"="*20}
System: {uname.system}
Machine: {uname.machine}
Processor: {cpu_name}
{"="*20} BOOT {"="*20}
Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}
Up Time: {up_time}
{"="*20} CPU {"="*20}
Physical cores: {psutil.cpu_count(logical=False)}
Total cores: {psutil.cpu_count(logical=True)}
Current Frequency: {cpufreq.current:.2f}Mhz
Total CPU Usage: {psutil.cpu_percent()}%
{"="*20} MEMORY {"="*20}
Total: {get_size(svmem.total)}
Available: {get_size(svmem.available)}
Used: {get_size(svmem.used)}
Percentage: {svmem.percent}%
Swap Percentage: {swap.percent}%
{"="*20} DISK {"="*20}
Disk Usage: {round(perc_num, 2)}%
Used: {get_size(round(used_num, 2))}/{get_size(round(total_num, 2))}
Total read: {get_size(disk_io.read_bytes)}
Total write: {get_size(disk_io.write_bytes)}
{"="*20} Network {"="*20}
Total Bytes Sent: {get_size(net_io.bytes_sent)}
Total Bytes Received: {get_size(net_io.bytes_recv)}
```"""
	embed_json = {
		'timestamp': datetime.now(tz=timezone.utc).isoformat(),
		'footer': {
			'text': 'Updated: '
		},
		'color': 65311,
		'type': 'rich',
		'description': info,
		'title': 'Server info'
	}
	return embed_json

def test_wh_file():
	try:
		with open(f'../webhooks.yaml') as file2:
			yaml_dict = yaml.full_load(file2)
			webhooks = yaml_dict['webhooks']
			cycle = yaml_dict['Update_cycle']
			if type(webhooks) is not list:
				print('No webhooks found')
				sys.exit(0)
			for i in webhooks:
				if 'messages' not in i:
					data = {
						"embeds": [{
				'color': 65311,
				'type': 'rich',
				'description': 'temp',
				'title': 'Server info'}]
					}
					r = requests.post(url=i, json=data)
					print(r)
			print('Webhooks posted, please make them message specific')
	except Exception as e:
		print(e)
		webhooks = []
		cycle = 10
		with open('../webhooks.yaml', 'w') as file:
			file.write('# The update cycle is in seconds\n')
			file.write('Update_cycle: 10\n')
			file.write('# Webhook list will be checked every 10 cycles\n')
			file.write('# To add a webhook use "- https://discord.com/api/webhooks/<token>/messages/<message id>\n')
			file.write('webhooks: \n - null\n')
		print('No webhook file found, new one generated')
		sys.exit(0)

curr_cycle = 0
async def csmas_handler():
	while True:
		global webhooks, cycle, curr_cycle
		curr_cycle += 1
		if curr_cycle > 9:
			curr_cycle = 0
		for i in webhooks:
			if i is None:
				continue
			if 'messages' not in i:
				continue
			data = {
				"embeds": [get_sys_info()]
			}
			try:
				r = requests.patch(url=i, json=data)
				print(r)
				if str(r) == '<Response [400]>':
					print(r.text)
			except Exception as e:
				print(e)
		await asyncio.sleep(cycle)
def run():
	test_wh_file()
	asyncio.run(csmas_handler())

