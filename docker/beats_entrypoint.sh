echo "--> Starting beats process"
celery -A ideagram.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
