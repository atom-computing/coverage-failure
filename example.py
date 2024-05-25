import asyncio
import coverage


async def run():
    def raise_exception():
        raise RuntimeError("This is a test exception.")

    async def return_false():
        # simply returning false here causes the incorrectly missed line to be marked as hit
        try:
            await asyncio.to_thread(raise_exception)
            # raise RuntimeError("This is a test exception.")  # doing this instead will cause line below to show up
        finally:
            return False

    # remove this conditional also fixes the problem
    if await return_false():
        return False

    await asyncio.to_thread(print, "hello",)  # this line is incorrectly marked as missing the coverage report


if __name__ == '__main__':
    cov = coverage.Coverage(branch=False)
    cov.start()

    asyncio.run(run())

    cov.stop()
    cov.save()

    cov.report(show_missing=True)
