import { createRouter, createWebHistory } from 'vue-router';
import { getCurrentUser } from 'vuefire';

import SplashView from '@/views/SplashView.vue';
import TrendView from '@/views/TrendView.vue';
import RecordView from '@/views/RecordView.vue';
import ProfileView from '@/views/ProfileView.vue';
import DashboardView from '@/views/DashboardView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      redirect: '/splash',
      meta: {},
    },
    {
      path: '/splash',
      name: 'splash',
      component: SplashView,
      meta: {},
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/trends',
      name: 'trends',
      component: TrendView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/records',
      name: 'records',
      component: RecordView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
  ],
});

router.beforeEach(async (to, _, next) => {
  const isLoggedIn = (await getCurrentUser()) ? true : false;

  if (to.meta.requiresAuth) {
    if (!isLoggedIn) {
      next({ name: 'splash' });
    } else {
      next();
    }
  } else if (isLoggedIn && (to.path === '/' || to.path === '/splash')) {
    next({ name: 'dashboard' });
  } else {
    next();
  }
});

export default router;
