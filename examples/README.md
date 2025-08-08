# Locust Test Examples

This directory contains example Locust test scripts that you can use as starting points for your own load testing scenarios.

## Files Overview

### `simple_web_test.py`

A basic example showing:

- Simple HTTP GET/POST requests
- Multiple user classes in one file
- Task weighting (some tasks run more frequently)
- Basic form submission simulation
- API endpoint testing

**Use case**: General website load testing, API testing

### `advanced_load_test.py`

A more sophisticated example demonstrating:

- Custom load shapes (gradual ramp-up, spike testing)
- Data-driven testing using external JSON files
- User session management (login/logout)
- Error handling and logging
- Complex user workflows (browse → add to cart → checkout)

**Use case**: Production-like testing with realistic user behavior

### `test_data.json`

Sample test data file used by the advanced example:

- User credentials for login testing
- Product IDs for e-commerce simulation
- Search terms and API endpoints

## How to Use These Examples

1. **Choose an example** that matches your testing needs
2. **Copy the script** to your shared storage as `locustfile.py`
3. **Modify the script** to match your application's endpoints and behavior
4. **Upload test data** if using the advanced example
5. **Configure target host** in the Locust web UI
6. **Start your load test**

## Quick Start

1. Upload `simple_web_test.py` as `locustfile.py` to your Locust shared storage
2. Scale up your Locust master and workers:
   ```bash
   kubectl scale deployment locust-distributed-master --replicas=1
   kubectl scale deployment locust-distributed-worker --replicas=3
   ```
3. Port-forward to the Locust web UI:
   ```bash
   kubectl port-forward service/locust-distributed-master 8089:8089
   ```
4. Open http://localhost:8089 and configure your test

## Customization Tips

### Modifying Endpoints

Update the URLs in the `@task` methods to match your application:

```python
@task
def test_my_endpoint(self):
    self.client.get("/my-custom-endpoint")
```

### Adjusting Load Patterns

Change the `wait_time` to control user behavior:

```python
wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
```

### Task Weighting

Use numbers after `@task` to control frequency:

```python
@task(3)  # Runs 3x more often
def frequent_task(self):
    pass

@task(1)  # Runs less frequently
def rare_task(self):
    pass
```

### Custom Load Shapes

Use the load shape classes in `advanced_load_test.py` or create your own:

```python
class MyCustomShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()
        # Your custom logic here
        return (user_count, spawn_rate)
```

## Best Practices

1. **Start small**: Begin with a few users and gradually increase
2. **Monitor resources**: Watch CPU/memory usage of your target system
3. **Use realistic data**: Test with production-like data volumes
4. **Test incrementally**: Add complexity to your tests over time
5. **Document your tests**: Add comments explaining the business logic

## Need Help?

- [Locust Documentation](https://docs.locust.io/)
- [Locust Task Reference](https://docs.locust.io/en/stable/writing-a-locustfile.html)
- [Load Shape Documentation](https://docs.locust.io/en/stable/custom-load-shape.html)
