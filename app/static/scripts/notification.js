// navigation and filter for notification page

const notificationsMapping = [
  {
    id: "notificationPageAllNotificationsFilter",
    param: "all",
    supportedNotificationType: [
      "PostNotification",
      "CommentNotification",
      "Post",
    ],
    counterId: "notificationPageAllNotificationsCount",
  },
  {
    id: "notificationPagePostNotificationsFilter",
    param: "posts",
    supportedNotificationType: ["PostNotification"],
    counterId: "notificationPagePostNotificationsCount",
  },
  {
    id: "notificationPageCommentNotificationsFilter",
    param: "comments",
    supportedNotificationType: ["CommentNotification"],
    counterId: "notificationPageCommentNotificationsCount",
  },
  {
    id: "notificationPagePostStatusFilter",
    param: "post-status",
    supportedNotificationType: ["Post"],
    counterId: "notificationPagePostStatusCount",
  },
];

const notificationFilterContainer = document.querySelector(
  ".notification-section .filter-container",
);

const notificationFilter = () => {
  notificationsMapping.forEach((item) => {
    const filterButton = notificationFilterContainer?.querySelector(
      `#${item.id}`,
    );

    filterButton?.addEventListener("click", () => {
      window.location.href = `/notifications?filter=${item.param}`;
    });
  });
};

const getAllNotificationsCount = async () => {
  const userProfileModal = document.querySelector("#userProfileModal");

  if (!userProfileModal) return;

  const notificationCounter = userProfileModal?.querySelector(
    ".notification-count",
  );

  if (!notificationCounter) return;

  try {
    const response = await fetch("/api/notifications/count", {
      method: "GET",
    });

    const { status, notification_count } = await response.json();

    if (status !== 200) return;

    if (notification_count === 0) {
      notificationCounter.classList.add("d-none");
      notificationCounter.textContent = "";
    } else if (notification_count > 0) {
      notificationCounter.classList.remove("d-none");
      notificationCounter.textContent = notification_count;
      if (notification_count > 99) {
        notificationCounter.textContent = "99+";
      }
    }
  } catch (error) {
    console.error("Error getting all notifications count", error);
  }
};

document.addEventListener("DOMContentLoaded", () => {
  console.log("notification.js loaded");
  notificationFilter();
  getAllNotificationsCount();
});

// update notification status
const notificationContentContainer = document.querySelector(
  ".notification-section #notificationPageNotificationContentContainer",
);

const updateNotificationStatus = async (notificationId, notificationType) => {
  try {
    const response = await fetch(`/api/notifications/${notificationId}`, {
      method: "PUT",
      body: JSON.stringify({ type: notificationType }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const { status, post_detail_url, post_status } = await response.json();

    if (status === 200) {
      window.open(post_detail_url, "_blank");
    } else {
      throw new Error("Error updating notification status");
    }

    return {
      status,
      post_detail_url,
      postStatus: post_status || null,
    };
  } catch (error) {
    console.error("Error updating notification status", error);
  }
};

const updateNotificationCounter = (notificationType) => {
  notificationsMapping.forEach(({ supportedNotificationType, counterId }) => {
    const notificationCounter = notificationFilterContainer?.querySelector(
      `#${counterId}`,
    );

    if (
      !supportedNotificationType.includes(notificationType) ||
      !notificationCounter
    )
      return;

    const currentCount = parseInt(notificationCounter.textContent);

    notificationCounter.textContent = currentCount - 1;
    const newCount = parseInt(notificationCounter.textContent);

    if (newCount === 0) {
      notificationCounter.classList.add("d-none");
    } else if (newCount > 0) {
      notificationCounter.classList.remove("d-none");

      if (newCount > 99) notificationCounter.textContent = "99+";
    }

    return;
  });
};

document.addEventListener("notificationPaginationLoaded", () => {
  const notificationContentContainer = document.querySelector(
    ".notification-section #notificationPageNotificationContentContainer",
  );

  [...notificationContentContainer?.children].forEach((notification) => {
    const notificationType = notification.getAttribute(
      "data-notification-type",
    );
    const notificationId = notification.id;

    if (!notificationType || !notificationId) return;

    notification.addEventListener("click", async () => {
      try {
        const { status, post_detail_url, postStatus } =
          await updateNotificationStatus(notificationId, notificationType);

        if (status !== 200) {
          throw new Error("Error updating notification status");
        }

        window.open(post_detail_url, "_blank");

        if (postStatus && postStatus === "Pending") return;

        notification.classList.add("read");
        updateNotificationCounter(notificationType);
      } catch (error) {
        console.error("Error updating notification status", error);
      }
    });
  });
});