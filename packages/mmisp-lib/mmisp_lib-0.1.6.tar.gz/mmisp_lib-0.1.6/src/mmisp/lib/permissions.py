from enum import StrEnum


class Permission(StrEnum):
    ADD = "add"
    MODIFY = "modify"
    """Manage Own Events."""
    MODIFY_ORG = "modify_org"
    """Manage Organisation Events."""
    PUBLISH = "publish"
    """Publish Organisation Events."""
    DELEGATE = "delegate"
    """Allow users to create delegation requests for their own org only events to trusted third parties."""
    SYNC = "sync"
    """Synchronisation permission, can be used to connect two MISP instances create data on behalf of other users.
    Make sure that the role with this permission has also access to tagging and tag editing rights."""
    ADMIN = "admin"
    """Limited organisation admin - create, manage users of their own organisation."""
    AUDIT = "audit"
    """Access to the audit logs of the user\'s organisation."""
    AUTH = "auth"
    """Users with this permission have access to authenticating via their Auth keys,
    granting them access to the API."""
    SITE_ADMIN = "site_admin"
    """Unrestricted access to any data and functionality on this instance."""
    REGEXP_ACCESS = "regexp_access"
    """Users with this role can modify the regex rules affecting how data is fed into MISP.
    Make sure that caution is advised with handing out roles that include this permission,
    user controlled executed regexes are dangerous."""
    TAGGER = "tagger"
    """Users with roles that include this permission can attach
    or detach existing tags to and from events/attributes."""
    TEMPLATE = "template"
    """Create or modify templates, to be used when populating events."""
    SHARING_GROUP = "sharing_group"
    """Permission to create or modify sharing groups."""
    TAG_EDITOR = "tag_editor"
    """This permission gives users the ability to create tags."""
    SIGHTING = "sighting"
    """Permits the user to push feedback on attributes into MISP by providing sightings."""
    OBJECT_TEMPLATE = "object_template"
    """Create or modify MISP Object templates."""
    PUBLISH_ZMQ = "publish_zmq"
    """Allow users to publish data to the ZMQ pubsub channel via the publish event to ZMQ button."""
    PUBLISH_KAFKA = "publish_kafka"
    """Allow users to publish data to Kafka via the publish event to Kafka button."""
    DECAYING = "decaying"
    """Create or modify MISP Decaying Models."""
    GALAXY_EDITOR = "galaxy_editor"
    """Create or modify MISP Galaxies and MISP Galaxies Clusters."""
    WARNINGLIST = "warninglist"
    """Allow to manage warninglists."""
    VIEW_FEED_CORRELATIONS = "view_feed_correlations"
    """Allow the viewing of feed correlations. Enabling this can come at a performance cost."""
