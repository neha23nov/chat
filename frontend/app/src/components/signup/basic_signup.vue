<template>
  <div class="bg-container">
    <div class="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">
      <h2 class="text-2xl sm:text-2xl font-semibold text-center text-gray-800 mb-4">
        Get started with <span class="logo">WotNot</span>
      </h2>

      <hr class="my-3 border-gray-300" />

      <div class="space-y-4">
        <div class="w-full">
          <label for="username" class="block text-sm font-medium text-gray-700">Business Name</label>
          <input type="text" id="username" v-model="username"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="email" class="block text-sm font-medium text-gray-700">Business Email Address</label>
          <input type="email" id="email" v-model="email"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" v-model="password" placeholder="Set Password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
          <div class="h-2 mt-2 rounded transition-all duration-300" :style="{ width: strengthWidth, backgroundColor: strengthColor }"></div>
          <p class="text-sm mt-1 font-medium" :style="{ color: strengthColor }">{{ strengthLabel }}</p>
        </div>

        <div class="mt-4 text-sm text-center">
          <p class="mb-2 text-sm">
            By signing up you agree to the
            <router-link to="/terms-and-privacy#terms-and-conditions" class="text-[#075e54] font-semibold">Terms</router-link>
            and
            <router-link to="/terms-and-privacy#privacy-policy" class="text-[#075e54] font-semibold">Privacy Policy</router-link>
          </p>
        </div>
      </div>

      <div class="cf-turnstile" data-sitekey="0x4AAAAAAB4JZr-MpJxScC4y"></div>

      <div class="flex flex-col items-center">
        <button
          class="w-full bg-gradient-to-r from-[#075e54] via-[#089678] to-[#075e54] text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:from-[#078478] hover:via-[#08b496] hover:to-[#078478] transition-all duration-300"
          @click.prevent="handleSubmit"
        >
          Get Account
        </button>

        <p class="mt-4 text-center text-sm">
          Already have an account?
          <a href="" class="text-[#075e54] font-semibold mb-4" @click.prevent="redirectLogin">Login</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import zxcvbn from "zxcvbn";

export default {
  name: "BasicSignUpForm",
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL || "http://localhost:8000", // Backend URL
      username: "",
      email: "",
      password: "",
    };
  },
  computed: {
    strengthScore() {
      return zxcvbn(this.password || "").score;
    },
    strengthLabel() {
      return ["Very Weak", "Weak", "Fair", "Good", "Strong"][this.strengthScore];
    },
    strengthColor() {
      return ["#e53e3e", "#dd6b20", "#d69e2e", "#38a169", "#3182ce"][this.strengthScore];
    },
    strengthWidth() {
      return `${(this.strengthScore / 4) * 100}%`;
    },
  },
  mounted() {
    const script = document.createElement("script");
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  },
  methods: {
    async handleSubmit() {
      const token = document.querySelector('input[name="cf-turnstile-response"]')?.value;
      if (!token) {
        alert("Please complete the CAPTCHA.");
        return;
      }

      if (!this.username || !this.email || !this.password) {
        alert("Please fill in all required fields.");
        return;
      }

      const formData = {
        username: this.username,
        email: this.email,
        password: this.password,
        cf_token: token,
        WABAID: null,
        PAccessToken: null,
        Phone_id: null,
      };

      try {
        const response = await fetch(`${this.apiUrl}/auth/register`, { // ✅ Corrected URL
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        });

        const data = await response.json();

        if (response.ok) {
          alert("Account created successfully!");
          this.username = "";
          this.email = "";
          this.password = "";
        } else {
          alert(data.detail || "Failed to create account. Please try again.");
        }
      } catch (error) {
        console.error(error);
        alert("Error connecting to server.");
      }
    },
    redirectLogin() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.logo {
  font-weight: 800;
  margin: 8px 0;
  padding-right: 30px;
  font-size: 30px;
  color: #075e54;
}
.bg-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-image: url("@/assets/LoginPage.png");
  background-position: center;
  padding: 0 16px;
}
</style>
