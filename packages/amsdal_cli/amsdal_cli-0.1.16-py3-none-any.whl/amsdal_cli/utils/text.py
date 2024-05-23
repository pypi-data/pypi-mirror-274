from rich import prompt


def rich_warning(text: str) -> str:
    return f'[dark_orange]{text}[/dark_orange]'


def rich_info(text: str) -> str:
    return f'[blue]{text}[/blue]'


def rich_highlight(text: str) -> str:
    return f'[dark_cyan]{text}[/dark_cyan]'


def rich_error(text: str) -> str:
    return f'[red]{text}[/red]'


def rich_success(text: str) -> str:
    return f'[green]{text}[/green]'


def rich_highlight_version(text: str) -> str:
    return f'[orange3]{text}[/orange3]'


def rich_command(text: str) -> str:
    return f'[dark_green]{text}[/dark_green]'


class CustomConfirm(prompt.Confirm):
    def process_response(self, value: str) -> bool:
        """Convert choices to a bool."""
        value = value.strip().lower()
        if value not in [c.lower() for c in self.choices]:
            raise prompt.InvalidResponse(self.validate_error_message)
        return value == self.choices[0]
