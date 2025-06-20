from hevy_api import ApiRequest
from datetime import datetime
from rich import box
from rich.table import Table
from rich.console import Console


def pick_color(item, name):
    if name == "delta":
        if (item.seconds / 3600) >= 2:
            return f"[yellow]{str(item)}[/yellow]"
        elif (item.seconds / 3600) >= 1:
            return f"[green]{str(item)}[/green]"
        else:
            return str(item)

    if name == "total_weight":
        if item >= 20000:
            return f"[yellow]{item:.2f}[/yellow]"
        elif item >= 10000:
            return f"[green]{item:.2f}[/green]"
        else:
            return f"{item:.2f}"


def pretty_dt(dt, ts=False):
    input_fmt = "%Y-%m-%dT%H:%M:%S%z"
    if ts:
        pretty_fmt = "%a %b %d %Y %H:%M"
    else:
        pretty_fmt = "%a %b %d %Y"
    return datetime.strptime(dt, input_fmt).strftime(pretty_fmt)


def display_workout_table(workouts, console, show_accolades=False):
    input_fmt = "%Y-%m-%dT%H:%M:%S%z"

    ## Define the table
    table = Table(title="Workouts")
    table.add_column("#")
    table.add_column("Title")
    table.add_column("# of Exercises", justify="right")
    table.add_column("Total Sets", justify="right")
    table.add_column("Total Reps", justify="right")
    table.add_column("Total Weight (KG)", justify="right")
    table.add_column("Session")
    table.add_column("Time Spent")

    ## Get the workout count
    workout_count = api.get_workout_count()
    print(f"Workout count is: {workout_count}")

    ## Add each workout as a table row
    best_total_weight = [0, None]
    best_total_reps = [0, None]
    best_total_sets = [0, None]
    all_time = {"weight": 0, "reps": 0, "sets": 0, "workouts": 0, "time_spent": 0}

    for i, workout in enumerate(reversed(workouts)):
        ## Define time formats for deltas
        total_weight = 0
        total_exercises = 0
        total_sets = 0
        total_reps = 0

        for exercise in workout["exercises"]:
            total_exercises += 1
            for eset in exercise["sets"]:
                total_sets += 1
                if eset["weight_kg"] and eset["reps"]:
                    total_reps += eset["reps"]
                    total_weight += eset["weight_kg"] * eset["reps"]
                    # print(f"Calculated total weight with {exercise['title']}: {eset['weight_kg']} * {eset['reps']} = {total_weight} KG")

        best_total_weight = (
            [total_weight, pretty_dt(workout["end_time"])]
            if total_weight > best_total_weight[0]
            else best_total_weight
        )
        best_total_reps = (
            [total_reps, pretty_dt(workout["end_time"])]
            if total_reps > best_total_reps[0]
            else best_total_reps
        )
        best_total_sets = (
            [total_sets, pretty_dt(workout["end_time"])]
            if total_sets > best_total_sets[0]
            else best_total_sets
        )

        ## Strip out emojis, and convert time strings to DT to calculate Delta
        title_no_emoji = workout.get("title").encode("ascii", "ignore").decode()
        delta = datetime.strptime(
            workout.get("end_time"), input_fmt
        ) - datetime.strptime(workout.get("start_time"), input_fmt)
        start_time = pretty_dt(workout.get("start_time"), ts=True)
        end_time = datetime.strptime(workout.get("end_time"), input_fmt).strftime(
            "%H:%M"
        )

        all_time["workouts"] += 1
        all_time["weight"] += total_weight
        all_time["reps"] += total_reps
        all_time["sets"] += total_sets
        all_time["time_spent"] += delta.seconds

        table.add_row(
            str(i + 1),
            title_no_emoji,
            str(total_exercises),
            str(total_sets),
            str(total_reps),
            pick_color(total_weight, "total_weight"),
            f"{start_time} -> {end_time}",
            pick_color(delta, "delta"),
        )

    console.print(table)

    if show_accolades:
        table_accolades = Table(title="Accolades", box=box.SIMPLE_HEAD)

        table_accolades.add_column("Name")
        table_accolades.add_column("Score")
        table_accolades.add_column("Date")

        table_accolades.add_row(
            "Best Total Reps", f"{best_total_reps[0]:,}", best_total_reps[1]
        )
        table_accolades.add_row(
            "Best Total Sets", f"{best_total_sets[0]:,}", best_total_sets[1]
        )
        table_accolades.add_row(
            "Best Total Weight", f"{best_total_weight[0]:,} kg", best_total_weight[1]
        )
        table_accolades.add_row("Number of Workouts", f"{all_time['workouts']:,}", "-")
        table_accolades.add_row(
            "Total Time Working out", f"{all_time['time_spent'] / 3600:.2f} hours", "-"
        )
        table_accolades.add_row("All time Reps", f"{all_time['reps']:,}", "-")
        table_accolades.add_row("All time Sets", f"{all_time['sets']:,}", "-")
        table_accolades.add_row("All time Weight", f"{all_time['weight']:,} kg", "-")

        console.print("")
        console.print(table_accolades)


if __name__ == "__main__":
    api = ApiRequest()
    console = Console()
    workouts = api.list_workouts()
    display_workout_table(workouts, console, show_accolades=True)
