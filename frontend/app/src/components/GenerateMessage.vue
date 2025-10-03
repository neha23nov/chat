<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-50">
    <div class="w-full max-w-lg bg-white rounded-xl shadow-md p-6">
      <h2 class="text-xl font-semibold text-green-800 mb-4">
        ✨  Message
      </h2>

      <!-- Input -->
      <textarea
        v-model="prompt"
        placeholder="Type your prompt here... e.g. Diwali wish"
        class="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
        rows="4"
      ></textarea>

      <!-- Button -->
      <button
        @click="generateMessage"
        class="mt-4 w-full bg-green-700 text-white py-2 px-4 rounded-lg hover:bg-green-800 transition"
      >
        Generate Message
      </button>

      <!-- Output -->
      <div v-if="generatedMessage" class="mt-6">
        <h3 class="font-medium text-gray-700">Generated Message:</h3>
        <div class="bg-gray-100 border border-gray-300 rounded-lg p-4 mt-2">
          {{ generatedMessage }}
        </div>
      </div>

      <!-- Error -->
      <p v-if="error" class="mt-4 text-red-600">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "GenerateMessage",
  data() {
    return {
      prompt: "",
      generatedMessage: "",
      error: "",
    };
  },
  methods: {
    async generateMessage() {
      try {
        this.error = "";
        const response = await axios.post("http://localhost:8000/message/generate", {
          prompt: this.prompt,
        });
        this.generatedMessage = response.data.message;
      } catch (err) {
        this.error = "⚠️ Could not generate message. Please try again.";
      }
    },
  },
};
</script>
