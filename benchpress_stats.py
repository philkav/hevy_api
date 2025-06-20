from hevy_api import ApiRequest
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def extract_workout(workout_name, workouts):
    my_workouts = {}
    for workout in workouts:
        creation = workout['created_at']
        for exercise in workout['exercises']:
            if exercise['title'] == workout_name:
                my_workouts[creation] = exercise

    return my_workouts



def show_formatted(workouts):
    colormap = {'warmup': 'dim yellow', 'normal': 'bold green', 'dropset': 'blue', 'failure': 'red'}
    for date in workouts.keys():
        dt = datetime.fromisoformat(date).strftime('%B %d %Y')
        note = workouts[date].get('notes', 'No Notes')
        note = 'No Notes' if len(note) < 1 else note
        table = Table(title=f"[blue][{dt}][/blue]: [bold]{note}[/bold]", min_width=120, title_justify='left')
        table.add_column("#")
        table.add_column("Type")
        table.add_column("Weight")
        table.add_column("Reps")

        for workset in workouts[date]['sets']:
            table.add_row(str(workset['index']), workset['type'], str(workset['weight_kg']), str(workset['reps']), style=colormap.get(workset['type']))

        console.print("\n")
        console.print(table)


if __name__ == "__main__":
    api = ApiRequest()
    workouts = reversed(api.list_workouts())
    benchpress = extract_workout('Bench Press (Barbell)', workouts)
    show_formatted(benchpress)
