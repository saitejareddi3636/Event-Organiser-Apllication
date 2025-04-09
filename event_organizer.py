from kivy.app import App
from kivy.uix.boxlayout import BoxLayout  
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from plyer import notification  # For notifications
from datetime import datetime, timedelta  # For date handling
from app import setup_database, add_to_favorites, get_favorites, share_event, get_shared_events  # Added share_event, get_shared_events

current_user_id = None  # Simulating logged-in user

class LoginScreen(BoxLayout):
    # (Same as before)
    ...

class EventManagerScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=20, padding=[50, 50, 50, 50], **kwargs)

        self.add_widget(Label(text="Event Manager", font_size=24, size_hint=(1, 0.2)))

        self.event_name_input = TextInput(hint_text='Event Name', size_hint=(1, 0.1))
        self.add_widget(self.event_name_input)

        self.event_date_input = TextInput(hint_text='Event Date (YYYY-MM-DD)', size_hint=(1, 0.1))
        self.add_widget(self.event_date_input)

        self.event_location_input = TextInput(hint_text='Location', size_hint=(1, 0.1))
        self.add_widget(self.event_location_input)

        add_event_button = Button(text='Add Event', size_hint=(1, 0.2))
        add_event_button.bind(on_release=self.add_event)
        self.add_widget(add_event_button)

        view_favorites_button = Button(text='View Favorites', size_hint=(1, 0.2))
        view_favorites_button.bind(on_release=self.view_favorites)
        self.add_widget(view_favorites_button)

        view_shared_button = Button(text='View Shared Events', size_hint=(1, 0.2))
        view_shared_button.bind(on_release=self.view_shared_events)
        self.add_widget(view_shared_button)

    def add_event(self, instance):
        # (Same as before)
        ...

    def view_favorites(self, instance):
        # (Same as before)
        ...

    def view_shared_events(self, instance):
        """Displays events shared with the current user."""
        shared_events = get_shared_events(current_user_id)
        content = BoxLayout(orientation='vertical')
        for event in shared_events:
            content.add_widget(Label(text=f"From: {event[4]}, Event: {event[1]} on {event[2]} at {event[3]}"))
        popup = Popup(title="Shared Events", content=content, size_hint=(0.8, 0.6))
        popup.open()

    def show_popup(self, title, message):
        # (Same as before)
        ...

class ShareEventScreen(BoxLayout):
    """Screen to share an event with another user."""
    def __init__(self, event_id, **kwargs):
        super().__init__(orientation='vertical', spacing=20, padding=[50, 50, 50, 50], **kwargs)

        self.event_id = event_id

        self.add_widget(Label(text="Share Event", font_size=24, size_hint=(1, 0.2)))

        self.username_input = TextInput(hint_text="Recipient's Username", size_hint=(1, 0.1))
        self.add_widget(self.username_input)

        share_button = Button(text='Share', size_hint=(1, 0.2))
        share_button.bind(on_release=self.share_event)
        self.add_widget(share_button)

    def share_event(self, instance):
        recipient_username = self.username_input.text
        result = share_event(current_user_id, recipient_username, self.event_id)
        notification.notify(
            title="Share Event",
            message=result,
            timeout=5
        )
        self.show_popup("Share Event", result)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

class EventOrganizerApp(App):
    def build(self):
        setup_database()
        root = BoxLayout(orientation='vertical')
        root.add_widget(LoginScreen())
        return root


if __name__ == '__main__':
    EventOrganizerApp().run()
