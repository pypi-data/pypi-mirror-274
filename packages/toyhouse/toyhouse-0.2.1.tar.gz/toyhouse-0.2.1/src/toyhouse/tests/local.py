import toyhouse
session = toyhouse.Session("ceruloryx", "Winterwatcher566")
session.auth()


forum_info = toyhouse.Forum(session, 5867)
print(forum_info.posts)