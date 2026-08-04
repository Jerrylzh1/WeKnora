<template>
  <div class="login-layout">
    <!-- 公交线网知识图谱（背景光环，偏中放大） -->
    <div class="knowledge-network" aria-hidden="true">
      <svg class="kn-svg" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid slice" xmlns:xlink="http://www.w3.org/1999/xlink">
        <defs>
          <radialGradient id="knHubGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.5"/>
            <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
          </radialGradient>
        </defs>

        <!-- 径向支线 -->
        <g class="kn-spoke-group">
          <line class="kn-spoke" x1="300" y1="300" x2="530" y2="300"/>
          <line class="kn-spoke" x1="300" y1="300" x2="499" y2="415"/>
          <line class="kn-spoke" x1="300" y1="300" x2="415" y2="499"/>
          <line class="kn-spoke" x1="300" y1="300" x2="300" y2="530"/>
          <line class="kn-spoke" x1="300" y1="300" x2="185" y2="499"/>
          <line class="kn-spoke" x1="300" y1="300" x2="101" y2="415"/>
          <line class="kn-spoke" x1="300" y1="300" x2="70"  y2="300"/>
          <line class="kn-spoke" x1="300" y1="300" x2="101" y2="185"/>
          <line class="kn-spoke" x1="300" y1="300" x2="185" y2="101"/>
          <line class="kn-spoke" x1="300" y1="300" x2="300" y2="70"/>
          <line class="kn-spoke" x1="300" y1="300" x2="415" y2="101"/>
          <line class="kn-spoke" x1="300" y1="300" x2="499" y2="185"/>
        </g>

        <!-- 内环（琥珀） -->
        <circle class="kn-ring kn-ring--inner" cx="300" cy="300" r="150">
          <animate attributeName="stroke-dashoffset" from="0" to="-90" dur="14s" repeatCount="indefinite"/>
        </circle>
        <!-- 外环（白色虚线流动） -->
        <circle class="kn-ring" cx="300" cy="300" r="230">
          <animate attributeName="stroke-dashoffset" from="0" to="-120" dur="10s" repeatCount="indefinite"/>
        </circle>

        <!-- 站点节点 -->
        <circle class="kn-station" cx="530" cy="300" r="6" style="animation-delay:0s"/>
        <circle class="kn-station" cx="499" cy="415" r="6" style="animation-delay:.4s"/>
        <circle class="kn-station" cx="415" cy="499" r="6" style="animation-delay:.8s"/>
        <circle class="kn-station" cx="300" cy="530" r="6" style="animation-delay:1.2s"/>
        <circle class="kn-station" cx="185" cy="499" r="6" style="animation-delay:1.6s"/>
        <circle class="kn-station" cx="101" cy="415" r="6" style="animation-delay:2s"/>
        <circle class="kn-station" cx="70"  cy="300" r="6" style="animation-delay:2.4s"/>
        <circle class="kn-station" cx="101" cy="185" r="6" style="animation-delay:2.8s"/>
        <circle class="kn-station" cx="185" cy="101" r="6" style="animation-delay:3.2s"/>
        <circle class="kn-station" cx="300" cy="70"  r="6" style="animation-delay:3.6s"/>
        <circle class="kn-station" cx="415" cy="101" r="6" style="animation-delay:4s"/>
        <circle class="kn-station" cx="499" cy="185" r="6" style="animation-delay:4.4s"/>

        <!-- 中心枢纽 -->
        <circle class="kn-hub-glow" cx="300" cy="300" r="22" fill="url(#knHubGlow)"/>
        <circle class="kn-hub" cx="300" cy="300" r="13"/>
        <circle class="kn-hub-ring" cx="300" cy="300" r="18">
          <animate attributeName="r" values="18;26;18" dur="3.4s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.9;0;0.9" dur="3.4s" repeatCount="indefinite"/>
        </circle>

        <!-- 沿外环行驶的小巴 -->
        <g class="kn-bus-anim">
          <g transform="scale(0.95)">
            <ellipse class="kn-bus-shadow" cx="0" cy="16" rx="24" ry="5"/>
            <rect x="-24" y="-14" width="48" height="26" rx="6" fill="#ffffff"/>
            <rect x="-18" y="-9" width="11" height="8" rx="1.5" fill="#FFB300"/>
            <rect x="-4"  y="-9" width="11" height="8" rx="1.5" fill="#FFB300"/>
            <rect x="10"  y="-9" width="10" height="8" rx="1.5" fill="#FFB300"/>
            <rect x="-4"  y="2"  width="10" height="10" rx="1" fill="#7F1D1D"/>
            <circle cx="-12" cy="13" r="4" fill="#7F1D1D"/>
            <circle cx="12"  cy="13" r="4" fill="#7F1D1D"/>
          </g>
          <animateMotion dur="32s" repeatCount="indefinite" rotate="auto">
            <mpath href="#knRingPath" xlink:href="#knRingPath"/>
          </animateMotion>
        </g>
        <!-- 行驶路径（不可见，供 animateMotion 引用） -->
        <path id="knRingPath" d="M 70,300 a 230,230 0 1,0 460,0 a 230,230 0 1,0 -460,0" fill="none" stroke="none"/>
      </svg>
    </div>

    <!-- 左上角品牌 -->
    <a href="https://github.com/Tencent/WeKnora" target="_blank" class="header-logo" :title="$t('common.github')">
      <span class="brand-text">
        <span class="brand-name">北京公交</span>
        <span class="brand-sub">知识库</span>
      </span>
    </a>

    <!-- 左侧展示区 -->
    <div class="showcase-section">
      <div class="showcase-content">
        <div class="brand-badge">🚌 公交行业专属知识库</div>
        <h1 class="showcase-title">让公交运营知识，随问随答</h1>
        <p class="showcase-description">
          面向公交行业打造统一知识库，汇聚线路、调度、维修、安全与乘客服务等全场景资料，用 RAG
          问答与智能体，让每一次检索都快人一步。
        </p>

        <!-- 轮播（通俗优点介绍，玻璃卡） -->
        <div class="carousel-container">
          <swiper :modules="modules" :slides-per-view="1" :loop="true" :autoplay="{
            delay: 4000,
            disableOnInteraction: false,
          }" :effect="'fade'" :fade-effect="{ crossFade: true }"
            :pagination="{ clickable: true, dynamicBullets: false }" :speed="800" class="screenshot-swiper">
            <swiper-slide v-for="(slide, index) in slides" :key="index">
              <div class="kb-slide-card">
                <div class="kb-slide__icon">{{ ['📚', '🚀', '🚌', '🛡️'][index] }}</div>
                <div class="kb-slide__title">{{ slide.title }}</div>
                <div class="kb-slide__desc">{{ slide.description }}</div>
              </div>
            </swiper-slide>
          </swiper>
        </div>

        <div class="feature-tags">
          <span class="tag">{{ $t('platform.rag') }}</span>
          <span class="tag">{{ $t('platform.agent') }}</span>
          <span class="tag">{{ $t('platform.wiki') }}</span>
          <span class="tag">{{ $t('platform.hybridSearch') }}</span>
        </div>

        <div class="scenario-chips">
          <span class="chip">线路运营</span>
          <span class="chip">车辆维修</span>
          <span class="chip">安全规范</span>
          <span class="chip">乘客服务</span>
          <span class="chip">调度指挥</span>
        </div>

      </div>
    </div>

    <!-- 右侧表单区 -->
    <div class="form-section">
      <div class="form-panel">
        <!-- Login Card -->
        <div class="form-card" v-if="!isRegisterMode">
          <div class="form-header">
            <h2 class="form-title">{{ $t('auth.login') }}</h2>
            <p class="form-welcome">{{ $t('auth.subtitle') }}</p>
          </div>

          <div class="form-content">
            <t-form ref="formRef" :data="formData" :rules="formRules" @submit="handleLogin" layout="vertical"
              label-align="top">
              <t-form-item :label="$t('auth.email')" name="email">
                <t-input v-model="formData.email" :placeholder="$t('auth.emailPlaceholder')" type="text"
                  autocomplete="email" size="large" :disabled="loading" />
              </t-form-item>

              <t-form-item :label="$t('auth.password')" name="password">
                <t-input v-model="formData.password" :placeholder="$t('auth.passwordPlaceholder')" type="password"
                  autocomplete="current-password" size="large" :disabled="loading" @enter="handleLogin" />
              </t-form-item>

              <t-button type="submit" theme="primary" size="large" block :loading="loading" class="submit-button">
                {{ loading ? $t('auth.loggingIn') : $t('auth.login') }}
              </t-button>

              <div class="register-cta" v-if="registrationEnabled">
                <div class="register-cta__divider">
                  <span>{{ $t('auth.firstTime') }}</span>
                </div>
                <t-button theme="default" variant="outline" size="large" block class="register-cta__button"
                  :disabled="loading" @click="toggleMode">
                  {{ $t('auth.createAccount') }}
                </t-button>
              </div>

              <div v-if="oidcEnabled" class="oidc-divider">
                <span>{{ $t('auth.orContinueWith') }}</span>
              </div>

              <t-button v-if="oidcEnabled" theme="default" size="large" block :loading="oidcLoading" :disabled="loading"
                class="oidc-button" @click="handleOIDCLogin">
                {{ oidcLoading ? $t('auth.redirectingToOIDC') : oidcLoginText }}
              </t-button>
            </t-form>

            <!-- Features list -->
            <div class="login-features">
              <div class="feature-item">
                <span class="feature-icon">✓</span>
                <span class="feature-text">{{ $t('platform.multimodalParsing') }}</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">✓</span>
                <span class="feature-text">{{ $t('platform.hybridSearchEngine') }}</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">✓</span>
                <span class="feature-text">{{ $t('platform.ragQandA') }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Register Card -->
        <div class="form-card" v-if="isRegisterMode && (registrationEnabled || inviteLookup)">
          <div v-if="inviteLookup" class="invite-banner">
            <t-icon name="link" class="invite-banner__icon" />
            <div class="invite-banner__text">
              <div class="invite-banner__title">
                {{ $t('inviteRegister.bannerTitle', { tenant: inviteLookup.tenant_name || '' }) }}
              </div>
              <div class="invite-banner__hint">
                {{ $t('inviteRegister.bannerHint') }}
              </div>
            </div>
          </div>
          <div v-else-if="inviteLookupError" class="invite-banner invite-banner--error">
            {{ inviteLookupError }}
          </div>
          <div class="form-header">
            <h2 class="form-title">{{ $t('auth.createAccount') }}</h2>
            <p class="form-subtitle">{{ $t('auth.registerSubtitle') }}</p>
          </div>

          <div class="form-content">
            <t-form ref="registerFormRef" :data="registerData" :rules="registerRules" @submit="handleRegister"
              layout="vertical" label-align="top">
              <t-form-item :label="$t('auth.username')" name="username">
                <t-input v-model="registerData.username" :placeholder="$t('auth.usernamePlaceholder')" size="large"
                  :disabled="loading" />
              </t-form-item>

              <t-form-item :label="$t('auth.email')" name="email">
                <t-input v-model="registerData.email" :placeholder="$t('auth.emailPlaceholder')" type="text"
                  autocomplete="email" size="large" :disabled="loading" />
              </t-form-item>

              <t-form-item :label="$t('auth.password')" name="password">
                <t-input v-model="registerData.password" :placeholder="$t('auth.passwordPlaceholder')" type="password"
                  autocomplete="new-password" size="large" :disabled="loading" />
              </t-form-item>

              <t-form-item :label="$t('auth.confirmPassword')" name="confirmPassword">
                <t-input v-model="registerData.confirmPassword" :placeholder="$t('auth.confirmPasswordPlaceholder')"
                  type="password" autocomplete="new-password" size="large" :disabled="loading" @enter="handleRegister" />
              </t-form-item>

              <t-button type="submit" theme="primary" size="large" block :loading="loading" class="submit-button">
                {{ loading ? $t('auth.registering') : $t('auth.register') }}
              </t-button>
            </t-form>

            <div class="form-footer">
              <span>{{ $t('auth.haveAccount') }}</span>
              <a href="#" @click.prevent="toggleMode" class="link-button">
                {{ $t('auth.backToLogin') }}
              </a>
            </div>

            <div class="login-features">
              <div class="feature-item">
                <span class="feature-icon">✓</span>
                <span class="feature-text">{{ $t('platform.independentTenant') }}</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">✓</span>
                <span class="feature-text">{{ $t('platform.fullApiAccess') }}</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">✓</span>
                <span class="feature-text">{{ $t('platform.knowledgeBaseManagement') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MessagePlugin } from 'tdesign-vue-next'
import { useRoleLabel } from '@/composables/useRoleLabel'
import { notifyLoginSuccess } from '@/utils/loginNotify'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, EffectFade, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/effect-fade'
import 'swiper/css/pagination'
import {
  login,
  register,
  getOIDCAuthorizationURL,
  getOIDCConfig,
  autoSetup,
  getAuthConfig,
  userInfoFromApi,
  getInvitationByToken,
  registerByInvite,
  type InviteLookup,
} from '@/api/auth'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'

// Import screenshot images
import screenshot1 from '@/assets/img/screenshot-1.svg'
import screenshot2 from '@/assets/img/screenshot-2.svg'
import screenshot3 from '@/assets/img/screenshot-3.svg'
import screenshot4 from '@/assets/img/screenshot-4.svg'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { t, tm, locale } = useI18n()
const { formatRole, roleIcon } = useRoleLabel()

// Swiper modules
const modules = [Autoplay, EffectFade, Pagination]

// Carousel slides data
const slides = [
  {
    image: screenshot4,
    title: '知识随手查',
    description: '线路、排班、保修手册，问一句就找到，不再翻一堆文档'
  },
  {
    image: screenshot2,
    title: '新人快速上手',
    description: '把老师傅的经验存进知识库，新司机、新调度员也能马上学会'
  },
  {
    image: screenshot3,
    title: '调度更省心',
    description: '客流、准点率、异常一站看全，排班决策有据可依'
  },
  {
    image: screenshot1,
    title: '安全有保障',
    description: '安全规范、应急预案随时可查，隐患早发现、早处理'
  }
]

// Form references
const formRef = ref()
const registerFormRef = ref()

// State management
const loading = ref(false)
const oidcLoading = ref(false)
const isRegisterMode = ref(false)
const showLanguageMenu = ref(false)
const oidcEnabled = ref(false)
const oidcProviderName = ref('')
// registrationEnabled defaults to true so that on first paint the Register
// link is visible; the actual mode is fetched from /auth/config in onMounted.
// In invite_only mode the link/card are hidden.
const registrationEnabled = ref(true)

// invite-link state. When the URL carries ?token=xxx we resolve it to
// the originating tenant + role and switch the form into a "register
// via invitation" mode. The token bypasses the normal invite_only
// gate — possessing it IS the authorisation. Submitting the register
// form with this set hits /auth/register-by-invite (auto-login on
// success) instead of /auth/register.
const inviteToken = ref('')
const inviteLookup = ref<InviteLookup | null>(null)
const inviteLookupError = ref('')
const inviteLookupLoading = ref(false)

// Language options
const languageOptions = [
  { value: 'zh-CN', label: '简体中文', shortLabel: '中文', flag: '🇨🇳' },
  { value: 'en-US', label: 'English', shortLabel: 'EN', flag: '🇺🇸' },
  { value: 'ru-RU', label: 'Русский', shortLabel: 'RU', flag: '🇷🇺' },
  { value: 'ko-KR', label: '한국어', shortLabel: '한국어', flag: '🇰🇷' }
]

const currentLanguage = computed(() => locale.value)
const oidcLoginText = computed(() => {
  if (oidcProviderName.value) {
    return t('auth.oidcLoginWithProvider', { provider: oidcProviderName.value })
  }
  return t('auth.oidcLogin')
})
const currentLangOption = computed(() => languageOptions.find(l => l.value === currentLanguage.value))

// Login form data
const formData = reactive<{ [key: string]: any }>({
  email: '',
  password: '',
})

// Register form data
const registerData = reactive<{ [key: string]: any }>({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Login form validation rules
const formRules = computed(() => ({
  email: [
    { required: true, message: t('auth.emailRequired'), type: 'error' },
    { email: true, message: t('auth.emailInvalid'), type: 'error' }
  ],
  password: [
    { required: true, message: t('auth.passwordRequired'), type: 'error' },
    { min: 8, message: t('auth.passwordMinLength'), type: 'error' },
    { max: 32, message: t('auth.passwordMaxLength'), type: 'error' },
    { pattern: /[a-zA-Z]/, message: t('auth.passwordMustContainLetter'), type: 'error' },
    { pattern: /\d/, message: t('auth.passwordMustContainNumber'), type: 'error' }
  ]
}))

// Register form validation rules
const registerRules = computed(() => ({
  username: [
    { required: true, message: t('auth.usernameRequired'), type: 'error' },
    { min: 2, message: t('auth.usernameMinLength'), type: 'error' },
    { max: 20, message: t('auth.usernameMaxLength'), type: 'error' },
    {
      pattern: /^[a-zA-Z0-9_\u4e00-\u9fa5]+$/,
      message: t('auth.usernameInvalid'),
      type: 'error'
    }
  ],
  email: [
    { required: true, message: t('auth.emailRequired'), type: 'error' },
    { email: true, message: t('auth.emailInvalid'), type: 'error' }
  ],
  password: [
    { required: true, message: t('auth.passwordRequired'), type: 'error' },
    { min: 8, message: t('auth.passwordMinLength'), type: 'error' },
    { max: 32, message: t('auth.passwordMaxLength'), type: 'error' },
    { pattern: /[a-zA-Z]/, message: t('auth.passwordMustContainLetter'), type: 'error' },
    { pattern: /\d/, message: t('auth.passwordMustContainNumber'), type: 'error' }
  ],
  confirmPassword: [
    { required: true, message: t('auth.confirmPasswordRequired'), type: 'error' },
    {
      validator: (val: string) => val === registerData.password,
      message: t('auth.passwordMismatch'),
      type: 'error'
    }
  ]
}))

// Toggle login/register mode
const toggleMode = () => {
  isRegisterMode.value = !isRegisterMode.value

  Object.keys(registerData).forEach(key => {
    (registerData as any)[key] = ''
  })
}

// Toggle language menu
const toggleLanguageMenu = () => {
  showLanguageMenu.value = !showLanguageMenu.value
}

// Select language
const selectLanguage = (lang: string) => {
  locale.value = lang
  localStorage.setItem('locale', lang)
  showLanguageMenu.value = false
  MessagePlugin.success(t('language.languageSaved'))
}

// Close language menu when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.language-switch')) {
    showLanguageMenu.value = false
  }
}

// Add click outside listener
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const persistLoginResponse = async (response: any) => {
  // Backend renamed `tenant` to `active_tenant` and added `memberships`
  // when tenant-level RBAC landed (issue #1303). The two are otherwise
  // identical — `active_tenant` is the tenant whose ID is encoded in the
  // JWT, defaulting to the user's home tenant on a fresh login.
  const activeTenant = response.active_tenant || response.tenant
  if (response.user && response.token) {
    // user.tenant_id must be the user's HOME tenant (the immutable row
    // on the users table); useHomeTenant() and the home-badge logic both
    // assume so. The ACTIVE tenant (which can differ from home when the
    // server honoured a remembered last-active-tenant preference) is
    // expressed separately via setSelectedTenant below.
    const homeTenantIdRaw = response.user.tenant_id ?? activeTenant?.id ?? ''
    authStore.setUser(userInfoFromApi(response.user, homeTenantIdRaw))
    authStore.setToken(response.token)
    if (response.refresh_token) {
      authStore.setRefreshToken(response.refresh_token)
    }
    if (activeTenant) {
      authStore.setTenant({
        id: String(activeTenant.id) || '',
        name: activeTenant.name || '',
        owner_id: response.user.id || '',
        created_at: activeTenant.created_at || new Date().toISOString(),
        updated_at: activeTenant.created_at || new Date().toISOString()
      })
    } else {
      authStore.setTenant(null)
    }
    if (Array.isArray(response.memberships)) {
      authStore.setMemberships(response.memberships)
    }
    // If the backend dropped us into a non-home tenant (honoured a
    // remembered "last active tenant" preference), set the override so
    // subsequent requests carry X-Tenant-ID and the UI stays consistent.
    // Otherwise clear any stale override left in localStorage by a
    // previous session for a different account.
    const activeIdNum = Number(activeTenant?.id)
    const homeIdNum = Number(homeTenantIdRaw)
    if (Number.isFinite(activeIdNum) && Number.isFinite(homeIdNum) && activeIdNum !== homeIdNum) {
      authStore.setSelectedTenant(activeIdNum, activeTenant?.name || null)
    } else {
      authStore.setSelectedTenant(null, null)
    }
  }

  // Pull runtime capabilities (including whether ordinary users may create
  // workspaces) before entering the main UI so create actions never flash
  // briefly when the deployment is invitation-only.
  await authStore.refreshFromAuthMe()
  await nextTick()
  router.replace(authStore.hasValidTenant ? '/platform/knowledge-bases' : '/onboarding/workspace')
}

const getBackendOIDCRedirectURI = () => `${window.location.origin}/api/v1/auth/oidc/callback`

const loadOIDCConfig = async () => {
  try {
    const response = await getOIDCConfig()
    oidcEnabled.value = !!response.success && !!response.enabled
    oidcProviderName.value = response.provider_display_name || ''
  } catch {
    oidcEnabled.value = false
    oidcProviderName.value = ''
  }
}

// loadAuthConfig fetches /auth/config and caches whether self-service
// registration is allowed. Failures fall back to "enabled" so a transient
// network glitch doesn't lock new users out of an open deployment.
const loadAuthConfig = async () => {
  try {
    const response = await getAuthConfig()
    registrationEnabled.value = response.registration_mode !== 'invite_only'
  } catch {
    registrationEnabled.value = true
  }
}

const handleOIDCLogin = async () => {
  try {
    oidcLoading.value = true
    const response = await getOIDCAuthorizationURL(getBackendOIDCRedirectURI())
    const authorizationURL = response.authorization_url

    if (!response.success || !authorizationURL) {
      MessagePlugin.error(response.message || t('auth.oidcLoginFailed'))
      return
    }

    window.location.href = authorizationURL
  } catch (error: any) {
    console.error('OIDC 登录跳转失败:', error)
    MessagePlugin.error(error.message || t('auth.oidcLoginFailed'))
  } finally {
    oidcLoading.value = false
  }
}

// Handle login
const handleLogin = async () => {
  try {
    const valid = await formRef.value?.validate()
    if (valid !== true) return

    loading.value = true

    const response = await login({
      email: formData.email,
      password: formData.password,
    })

    if (response.success) {
      await persistLoginResponse(response)
      notifyLoginSuccess(response, t, tm, formatRole, roleIcon)
    } else {
      MessagePlugin.error(response.message || t('auth.loginError'))
    }
  } catch (error: any) {
    console.error('登录错误:', error)
    MessagePlugin.error(error.message || t('auth.loginErrorRetry'))
  } finally {
    loading.value = false
  }
}

// Handle registration. Dispatches based on whether the user arrived
// with a share-link token: with token -> register-by-invite (auto-
// login on success); without -> the normal self-service register
// (drops back to the login form for the user to sign in).
const handleRegister = async () => {
  try {
    const valid = await registerFormRef.value?.validate()
    if (valid !== true) return

    loading.value = true

    if (inviteToken.value) {
      const response = await registerByInvite({
        token: inviteToken.value,
        username: registerData.username,
        email: registerData.email,
        password: registerData.password,
      })
      if (!response.success) {
        MessagePlugin.error(response.message || t('auth.registerFailed'))
        return
      }
      MessagePlugin.success(t('auth.registerSuccess'))
      // register-by-invite returns the same shape as login (token +
      // active_tenant + memberships), so reuse the login persistence
      // path — same store writes, same redirect target.
      await persistLoginResponse(response)
      return
    }

    const response = await register({
      username: registerData.username,
      email: registerData.email,
      password: registerData.password
    })

    if (response.success) {
      MessagePlugin.success(t('auth.registerSuccess'))

      // Switch to login mode and fill in email
      isRegisterMode.value = false
      formData.email = registerData.email

      // Clear register form
      Object.keys(registerData).forEach(key => {
        (registerData as any)[key] = ''
      })
    } else {
      MessagePlugin.error(response.message || t('auth.registerFailed'))
    }
  } catch (error: any) {
    console.error('注册错误:', error)
    MessagePlugin.error(error.message || t('auth.registerError'))
  } finally {
    loading.value = false
  }
}

// Check if already logged in; for lite edition, attempt transparent auto-setup
onMounted(async () => {
  // Share-link landing: ?token=xxx switches the form into invite-
  // register mode before any other auto-flow (logged-in redirect /
  // auto-setup / OIDC) gets a chance to redirect. Resolution failure
  // surfaces inline; the user can still log in normally if they
  // already have an account. We check this BEFORE the isLoggedIn
  // redirect so an existing session doesn't bounce the user to
  // /platform (and possibly back to /login if the session is stale),
  // dropping the invite token along the way.
  const tokenFromQuery = String(route.query.token || '').trim()
  if (tokenFromQuery) {
    inviteToken.value = tokenFromQuery
    inviteLookupLoading.value = true
    try {
      const resp = await getInvitationByToken(tokenFromQuery)
      if (resp.success && resp.data) {
        inviteLookup.value = resp.data
        // Token bypasses invite_only — show the register card even
        // when self-service registration is otherwise disabled.
        registrationEnabled.value = true
        isRegisterMode.value = true
      } else {
        inviteLookupError.value = resp.message || t('inviteRegister.invalidBody')
      }
    } catch {
      inviteLookupError.value = t('inviteRegister.invalidBody')
    } finally {
      inviteLookupLoading.value = false
    }
    // Don't run auto-setup when the user came in via an invite link —
    // they're explicitly trying to register, not bootstrap a Lite
    // single-user instance.
    loadOIDCConfig()
    return
  }

  if (authStore.isLoggedIn) {
    router.replace('/platform/knowledge-bases')
    return
  }

  const AUTO_SETUP_FAILED_KEY = 'weknora_auto_setup_failed'
  if (localStorage.getItem(AUTO_SETUP_FAILED_KEY) !== 'true') {
    try {
      const response = await autoSetup()
      if (response.success) {
        authStore.setLiteMode(true)
        await persistLoginResponse(response)
        return
      } else {
        localStorage.setItem(AUTO_SETUP_FAILED_KEY, 'true')
      }
    } catch {
      localStorage.setItem(AUTO_SETUP_FAILED_KEY, 'true')
    }
  }

  loadOIDCConfig()
  loadAuthConfig()
})
</script>

<style lang="less" scoped>
.login-layout {
  // 通过 TDesign 主题变量统一改主色为「北京公交红」
  --td-brand-color: #B91C1C;
  --td-brand-color-hover: #DC2626;
  --td-brand-color-active: #991B1B;
  --td-brand-color-light: rgba(185, 28, 28, 0.10);
  --td-brand-color-light-active: rgba(185, 28, 28, 0.20);

  display: flex;
  width: 100%;
  min-height: 100%;
  overflow: hidden;
  position: relative;
  background: linear-gradient(225deg,
      #4a0c0c 0%,
      #6b1111 18%,
      #8B1A1A 32%,
      #a32020 46%,
      #B91C1C 62%,
      #c93535 76%,
      #dc5555 88%,
      #ef7777 100%);

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      radial-gradient(circle at 18% 45%, rgba(255, 255, 255, 0.08) 0%, transparent 45%),
      radial-gradient(circle at 82% 55%, rgba(255, 200, 150, 0.07) 0%, transparent 50%);
    pointer-events: none;
  }
}

/* ===================== 公交线网知识图谱（偏中放大背景光环） ===================== */
.knowledge-network {
  position: absolute;
  left: 44%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 1240px;
  height: 1240px;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
  opacity: 0.6;
}

.kn-svg {
  width: 100%;
  height: 100%;
  display: block;
}

.kn-ring {
  fill: none;
  stroke: rgba(255, 255, 255, 0.66);
  stroke-width: 2;
  stroke-dasharray: 3 9;
  stroke-linecap: round;
}

.kn-ring--inner {
  stroke: rgba(255, 179, 0, 0.6);
  stroke-width: 1.6;
  stroke-dasharray: 2 7;
}

.kn-spoke {
  stroke: rgba(255, 255, 255, 0.32);
  stroke-width: 1.2;
}

.kn-station {
  fill: #ffffff;
  stroke: #FFC83A;
  stroke-width: 3;
  transform-box: fill-box;
  transform-origin: center;
  animation: knPulse 4.5s ease-in-out infinite;
}

@keyframes knPulse {
  0%, 100% { transform: scale(1); opacity: 0.85; }
  50% { transform: scale(1.45); opacity: 1; }
}

.kn-hub-glow {
  fill: rgba(255, 255, 255, 0.3);
  animation: knHub 3.4s ease-in-out infinite;
}

@keyframes knHub {
  0%, 100% { transform: scale(1); opacity: 0.65; }
  50% { transform: scale(1.5); opacity: 0; }
}

.kn-hub {
  fill: #ffffff;
}

.kn-hub-ring {
  fill: none;
  stroke: #FFC83A;
  stroke-width: 3;
}

.kn-bus-shadow {
  fill: rgba(0, 0, 0, 0.18);
}

@media (prefers-reduced-motion: reduce) {
  .kn-ring,
  .kn-station,
  .kn-hub-glow {
    animation: none !important;
  }

  .kn-bus-anim {
    display: none;
  }
}

/* 左上角品牌 */
.header-logo {
  position: fixed;
  top: 28px;
  left: 48px;
  z-index: 100;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;

  .brand-logo {
    width: 64px;
    height: 64px;
    flex-shrink: 0;
    filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.25));
  }

  .brand-text {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    gap: 8px;
    line-height: 1.04;
  }

  .brand-name {
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    font-family: var(--app-font-family);
    letter-spacing: 1px;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
  }

  .brand-sub {
    font-size: 22px;
    font-weight: 700;
    color: #FFD27A;
    font-family: var(--app-font-family);
    letter-spacing: 2px;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  }
}

/* 左侧展示区 */
.showcase-section {
  flex: 0 0 52%;
  display: flex;
  align-items: center;
  padding: 90px 20px 90px 48px;
  box-sizing: border-box;
  position: relative;
}

.showcase-content {
  width: 100%;
  max-width: 720px;
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  margin-bottom: 0;
}

.brand-badge {
  align-self: flex-start;
  display: inline-block;
  padding: 8px 18px;
  margin-bottom: 20px;
  border-radius: 20px;
  background: rgba(255, 179, 0, 0.18);
  border: 1px solid rgba(255, 179, 0, 0.45);
  color: #FFD27A;
  font-size: 16px;
  font-weight: 600;
  font-family: var(--app-font-family);
  letter-spacing: 0.3px;
}

.showcase-title {
  margin: 0 0 16px 0;
  font-size: 50px;
  line-height: 1.2;
  font-weight: 800;
  color: #ffffff;
  font-family: var(--app-font-family);
  letter-spacing: 1px;
  text-shadow: 0 2px 14px rgba(0, 0, 0, 0.28);
}

.showcase-description {
  font-size: 19px;
  color: rgba(255, 255, 255, 0.86);
  margin: 0 0 26px 0;
  line-height: 1.7;
  font-family: var(--app-font-family);
}

.feature-tags {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.tag {
  display: inline-block;
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 20px;
  color: #ffffff;
  font-size: 15.5px;
  font-weight: 500;
  font-family: var(--app-font-family);
}

.scenario-chips {
  display: flex;
  gap: 10px;
  margin-bottom: 0;
  flex-wrap: wrap;
}

.chip {
  display: inline-block;
  padding: 7px 16px;
  border-radius: 8px;
  background: rgba(255, 179, 0, 0.14);
  border: 1px solid rgba(255, 179, 0, 0.35);
  color: #FFE0A3;
  font-size: 15px;
  font-weight: 500;
  font-family: var(--app-font-family);
}

/* 轮播（玻璃卡，通俗优点介绍） */
.carousel-container {
  width: 100%;
  margin: 4px 0 24px;
}

.screenshot-swiper {
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.10);
  border: 1px solid rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
  padding: 22px 22px 42px;

  :deep(.swiper-wrapper) {
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  }

  :deep(.swiper-pagination) {
    bottom: 16px !important;
    z-index: 10;
  }

  :deep(.swiper-pagination-bullet) {
    width: 8px;
    height: 8px;
    background: rgba(255, 255, 255, 0.35);
    opacity: 1;
    transition: all 0.3s ease;
    margin: 0 4px !important;
  }

  :deep(.swiper-pagination-bullet-active) {
    background: #FFB300;
    width: 22px;
    border-radius: 4px;
  }
}

.kb-slide-card {
  min-height: 110px;
}

.kb-slide__icon {
  font-size: 28px;
  margin-bottom: 10px;
}

.kb-slide__title {
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 7px;
  font-family: var(--app-font-family);
  letter-spacing: 0.5px;
  text-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
}

.kb-slide__desc {
  font-size: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  font-family: var(--app-font-family);
}


/* 右侧表单区 */
.form-section {
  flex: 0 0 48%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 50px 40px 30px;
  box-sizing: border-box;
  position: relative;
}

.form-panel {
  width: 100%;
  max-width: 460px;
  margin-bottom: 0;
  position: relative;
  z-index: 2;
}

.form-card {
  background: rgba(255, 255, 255, 0.97);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.18);
  box-sizing: border-box;
  border: none;
  width: 100%;
}

.invite-banner {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  margin-bottom: 20px;
  border-radius: 10px;
  background: var(--td-bg-color-container-hover, rgba(0, 0, 0, 0.03));
  border: 1px solid var(--td-component-stroke);
  color: var(--td-text-color-primary);
}

.invite-banner__icon {
  margin-top: 2px;
  font-size: 18px;
  flex-shrink: 0;
  color: var(--td-text-color-secondary);
}

.invite-banner__text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.invite-banner__title {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--td-text-color-primary);
}

.invite-banner__hint {
  font-size: 12px;
  color: var(--td-text-color-secondary);
  line-height: 1.5;
}

.invite-banner--error {
  background: var(--td-error-color-1, rgba(220, 38, 38, 0.06));
  border-color: var(--td-error-color-3, rgba(220, 38, 38, 0.2));
  color: var(--td-error-color, #b91c1c);
  font-size: 13px;
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--td-text-color-primary);
  margin: 0 0 6px 0;
  font-family: var(--app-font-family);
}

.form-welcome {
  font-size: 13px;
  color: var(--td-text-color-secondary);
  margin: 0;
  font-family: var(--app-font-family);
}

.form-hint {
  margin: 10px 0 0;
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--td-success-color-light, rgba(21, 101, 192, 0.08));
  color: var(--td-brand-color-active);
  font-size: 12.5px;
  line-height: 1.5;
  font-family: var(--app-font-family);
}

.register-cta {
  margin-top: 8px;

  &__divider {
    position: relative;
    text-align: center;
    margin: 4px 0 14px;
    color: var(--td-text-color-secondary);
    font-size: 13px;
    font-family: var(--app-font-family);

    span {
      position: relative;
      z-index: 1;
      padding: 0 12px;
      background: rgba(255, 255, 255, 0.97);
    }

    &::before {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      top: 50%;
      border-top: 1px solid var(--td-component-stroke);
    }
  }

  &__button {
    height: 46px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;
    border-color: var(--td-brand-color);
    color: var(--td-brand-color);

    &:hover {
      border-color: var(--td-brand-color-active);
      color: var(--td-brand-color-active);
      background: var(--td-brand-color-light);
    }
  }
}

.form-subtitle {
  font-size: 13px;
  color: var(--td-text-color-secondary);
  margin: 0;
  font-family: var(--app-font-family);
}

.form-content {
  :deep(.t-form-item__label) {
    font-size: 14px;
    color: var(--td-text-color-primary);
    font-weight: 500;
    margin-bottom: 8px;
    font-family: var(--app-font-family);
    display: block;
    text-align: left;
  }

  :deep(.t-input) {
    border: 1px solid var(--td-component-stroke);
    border-radius: 8px;
    background: var(--td-bg-color-container);
    transition: all 0.2s;

    &:focus-within {
      border-color: var(--td-brand-color);
      box-shadow: 0 0 0 3px rgba(185, 28, 28, 0.15);
    }

    &:hover {
      border-color: var(--td-brand-color);
    }

    .t-input__inner {
      border: none !important;
      box-shadow: none !important;
      outline: none !important;
      background: transparent;
      font-size: 15px;
      font-family: var(--app-font-family);

      &:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
      }
    }

    .t-input__wrap {
      border: none !important;
      box-shadow: none !important;
    }
  }

  :deep(.t-form-item) {
    margin-bottom: 18px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  :deep(.t-form-item__control) {
    width: 100%;
  }
}

.submit-button {
  height: 46px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  font-family: var(--app-font-family);
  margin: 20px 0 16px 0;
}

.oidc-divider {
  position: relative;
  margin: 4px 0 6px;
  text-align: center;
  color: var(--td-text-color-placeholder);
  font-size: 12px;

  span {
    position: relative;
    z-index: 1;
    padding: 0 12px;
    background: rgba(255, 255, 255, 0.95);
  }

  &::before {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    top: 50%;
    border-top: 1px solid var(--td-component-stroke);
  }
}

.oidc-button {
  height: 46px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
}

.form-footer {
  text-align: center;
  font-size: 14px;
  color: var(--td-text-color-secondary);
  font-family: var(--app-font-family);
  margin-top: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--td-component-stroke);

  .link-button {
    color: var(--td-brand-color);
    text-decoration: none;
    margin-left: 4px;
    font-weight: 500;
    transition: all 0.2s;

    &:hover {
      color: var(--td-brand-color);
      text-decoration: underline;
    }
  }
}

.login-form-footer {
  border-bottom: none;
  padding-bottom: 8px;
  margin-top: 12px;
}

.login-features {
  margin-top: 20px;
  padding: 0;

  .feature-item {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    font-size: 13px;
    color: var(--td-text-color-secondary);
    font-family: var(--app-font-family);

    &:last-child {
      margin-bottom: 0;
    }

    .feature-icon {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--td-brand-color-light);
      color: var(--td-brand-color-active);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 700;
      margin-right: 10px;
      flex-shrink: 0;
    }

    .feature-text {
      line-height: 1.4;
    }
  }
}

/* 响应式 */
@media (max-width: 1024px) {
  .showcase-title { font-size: 40px; }

  .header-logo {
    top: 24px;
    left: 40px;

    .brand-logo { width: 56px; height: 56px; }
    .brand-name { font-size: 22px; }
    .brand-sub { font-size: 17px; }
  }

  .knowledge-network { width: 900px; height: 900px; opacity: 0.55; }
}

@media (max-width: 768px) {
  .login-layout { flex-direction: column; }

  .showcase-section {
    flex: 0 0 auto;
    min-height: 52vh;
    padding: 80px 24px 24px;
  }

  .showcase-content { max-width: 100%; }

  .header-logo {
    top: 20px;
    left: 30px;

    .brand-logo { width: 48px; height: 48px; }
    .brand-name { font-size: 16px; }
    .brand-sub { font-size: 13px; }
    .brand-tag { display: none; }
  }

  .showcase-title { font-size: 32px; margin-bottom: 16px; }
  .feature-tags { margin-bottom: 14px; }
  .scenario-chips { margin-bottom: 22px; }

  .form-section {
    flex: 0 0 auto;
    padding: 24px;
  }

  .form-card { padding: 32px 24px; }
  .form-title { font-size: 22px; }

  .knowledge-network { width: 680px; height: 680px; opacity: 0.5; }
}

@media (max-width: 480px) {
  .knowledge-network { display: none; }

  .showcase-section { padding: 70px 20px 20px; }
  .showcase-title { font-size: 26px; }

  .tag { font-size: 12px; padding: 6px 14px; }
  .chip { font-size: 11.5px; padding: 5px 12px; }

  .form-section { padding: 20px; }

  .header-logo {
    top: 16px;
    left: 20px;

    .brand-logo { width: 44px; height: 44px; }
    .brand-sub { font-size: 11px; }
  }

  .form-card { padding: 28px 20px; }
  .form-header { margin-bottom: 24px; }
}

@media (prefers-reduced-motion: reduce) {
  .kn-ring,
  .kn-station,
  .kn-hub-glow {
    animation: none !important;
    transition: none !important;
  }

  .knowledge-network { display: none; }
}
</style>

<style lang="less">
html[theme-mode="dark"] {
  .login-layout {
    background: linear-gradient(225deg,
        #2a0808 0%,
        #420a0a 18%,
        #5C0E0E 32%,
        #7a1212 46%,
        #991B1B 62%,
        #b52424 76%,
        #d13535 88%,
        #e85050 100%);
  }

  .brand-name { color: #ffffff; }

.tag {
    background: rgba(255, 255, 255, 0.12);
  }

  .scenario-chips .chip {
    background: rgba(255, 179, 0, 0.1);
  }

  .form-card {
    background: rgba(36, 36, 36, 0.97) !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4) !important;
  }

  .register-cta__divider span {
    background: rgba(36, 36, 36, 0.97);
  }

  .form-content :deep(.t-input) {
    background: var(--td-bg-color-page) !important;
    border-color: rgba(255, 255, 255, 0.1) !important;

    &:hover {
      border-color: var(--td-brand-color) !important;
    }

    &:focus-within {
      border-color: var(--td-brand-color) !important;
    }
  }

  .screenshot-swiper .swiper-pagination-bullet-active {
    background: #FFB300 !important;
  }

}
</style>
