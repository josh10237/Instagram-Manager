from screens import instagramManagerApp
import helpers as h
import cache as c

if __name__ == "__main__":
    h.new_API(c.retrieve_log_in('username'), c.retrieve_log_in('password'))
    instagramManagerApp().run()

