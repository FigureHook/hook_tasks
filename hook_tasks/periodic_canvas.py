from celery import chain, group, signature

__all__ = ("gsc_aggresive_check",)


gsc_aggresive_check = chain(
    group(
        signature(
            "hook_tasks.tasks.new_release_check.tasks.check_new_release_by_site_name",
            args=(site,),
        )
        for site in ("gsc", "native")
    ),
    signature(
        "hook_tasks.tasks.sns_post.plurk.tasks.post_new_releases_to_plurk",
        options={"countdown": 60},
    ),
)
