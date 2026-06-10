<script setup lang="ts">
import type { ErrorPageNote } from "@/pages/errors/error-pages.data";

defineProps<{
    notes: ErrorPageNote[];
}>();
</script>

<template>
    <div class="error-notes">
        <p
            v-for="note in notes"
            :key="note.text"
            :class="['error-note', note.tone ? `error-note--${note.tone}` : '']"
        >
            <i :class="note.icon"></i>
            <span>{{ note.text }}</span>
        </p>
    </div>
</template>
