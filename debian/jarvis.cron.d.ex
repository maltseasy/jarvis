#
# Regular cron jobs for the jarvis package
#
0 4	* * *	root	[ -x /usr/bin/jarvis_maintenance ] && /usr/bin/jarvis_maintenance
