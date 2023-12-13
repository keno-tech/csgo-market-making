from selenium import webdriver
import time

url = "https://buff.163.com/goods/781534?from=market#tab=selling"  # Replace with the target URL
requests_per_minute = 60  # Adjust as needed

# Start Chrome in headless mode (without GUI)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

try:
    start_time = time.time()

    while True:
        driver.get(url)
        elapsed_time = time.time() - start_time

        # Calculate the time to sleep between requests to achieve the desired rate
        time_to_sleep = 60 / requests_per_minute - elapsed_time % (60 / requests_per_minute)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

except KeyboardInterrupt:
    pass

finally:
    driver.quit()
