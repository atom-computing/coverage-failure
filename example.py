import asyncio
import coverage


async def run():
    def raise_exception():
        raise RuntimeError("This is a test exception.")

    async def return_false():
        # simply returning false eliminates the issue
        try:
            await asyncio.to_thread(raise_exception)
            # raise RuntimeError("This is a test exception.")  # doing this instead eliminates the issue
        finally:
            return False

    # removing this conditional also eliminates the issue
    if await return_false():
        return False

    await asyncio.to_thread(print, "hello")  # this line is incorrectly marked as missing in the coverage report


if __name__ == '__main__':
    cov = coverage.Coverage(branch=False)
    cov.start()

    asyncio.run(run())

    cov.stop()
    cov.save()

    cov.report(show_missing=True)
