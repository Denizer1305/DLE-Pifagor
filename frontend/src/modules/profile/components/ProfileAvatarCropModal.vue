<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from "vue";

interface Props {
    file: File;
    isSubmitting?: boolean;
}

interface Emits {
    (event: "cancel"): void;
    (event: "confirm", file: File): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const OUTPUT_SIZE = 512;
const canvasRef = ref<HTMLCanvasElement | null>(null);
const zoom = ref(1);
const horizontalPosition = ref(0);
const verticalPosition = ref(0);
const isPreparing = ref(false);

let image: HTMLImageElement | null = null;
let sourceUrl = "";

function drawPreview(): void {
    const canvas = canvasRef.value;

    if (!canvas || !image) {
        return;
    }

    const context = canvas.getContext("2d");

    if (!context) {
        return;
    }

    const scale = Math.max(
        OUTPUT_SIZE / image.naturalWidth,
        OUTPUT_SIZE / image.naturalHeight,
    ) * zoom.value;
    const width = image.naturalWidth * scale;
    const height = image.naturalHeight * scale;
    const horizontalRange = Math.max((width - OUTPUT_SIZE) / 2, 0);
    const verticalRange = Math.max((height - OUTPUT_SIZE) / 2, 0);
    const x = (OUTPUT_SIZE - width) / 2
        + horizontalRange * (horizontalPosition.value / 100);
    const y = (OUTPUT_SIZE - height) / 2
        + verticalRange * (verticalPosition.value / 100);

    context.clearRect(0, 0, OUTPUT_SIZE, OUTPUT_SIZE);
    context.drawImage(image, x, y, width, height);
}

function disposeSourceUrl(): void {
    if (sourceUrl) {
        URL.revokeObjectURL(sourceUrl);
        sourceUrl = "";
    }
}

function loadImage(file: File): void {
    disposeSourceUrl();
    zoom.value = 1;
    horizontalPosition.value = 0;
    verticalPosition.value = 0;
    sourceUrl = URL.createObjectURL(file);

    const nextImage = new Image();
    nextImage.onload = () => {
        image = nextImage;
        drawPreview();
    };
    nextImage.src = sourceUrl;
}

function exportCroppedFile(): Promise<File> {
    return new Promise((resolve, reject) => {
        const canvas = canvasRef.value;

        if (!canvas) {
            reject(new Error("Не удалось подготовить изображение."));
            return;
        }

        canvas.toBlob((blob) => {
            if (!blob) {
                reject(new Error("Не удалось подготовить изображение."));
                return;
            }

            const fileName = props.file.name.replace(/\.[^.]+$/, "") || "avatar";
            resolve(new File([blob], `${fileName}-cropped.webp`, {
                type: "image/webp",
            }));
        }, "image/webp", 0.92);
    });
}

async function confirmCrop(): Promise<void> {
    isPreparing.value = true;

    try {
        emit("confirm", await exportCroppedFile());
    } finally {
        isPreparing.value = false;
    }
}

watch(
    () => props.file,
    (file) => {
        loadImage(file);
    },
    { immediate: true },
);

watch([zoom, horizontalPosition, verticalPosition], () => {
    drawPreview();
});

onBeforeUnmount(() => {
    disposeSourceUrl();
});
</script>

<template>
    <Teleport to="body">
        <div
            class="profile-avatar-crop-overlay"
            @click.self="emit('cancel')"
        >
            <section
                class="profile-avatar-crop-modal"
                role="dialog"
                aria-modal="true"
                aria-labelledby="avatar-crop-title"
            >
                <header class="profile-avatar-crop-head">
                    <div>
                        <span class="profile-avatar-crop-topline">
                            <i class="fas fa-crop-simple"></i>
                            Редактирование фото
                        </span>
                        <h2 id="avatar-crop-title">Кадрировать аватар</h2>
                    </div>

                    <button
                        class="profile-avatar-crop-close"
                        type="button"
                        aria-label="Закрыть редактор"
                        @click="emit('cancel')"
                    >
                        <i class="fas fa-xmark"></i>
                    </button>
                </header>

                <div class="profile-avatar-crop-workspace">
                    <canvas
                        ref="canvasRef"
                        class="profile-avatar-crop-canvas"
                        :width="OUTPUT_SIZE"
                        :height="OUTPUT_SIZE"
                    ></canvas>

                    <div class="profile-avatar-crop-controls">
                        <label class="profile-avatar-crop-control">
                            <span>
                                <i class="fas fa-magnifying-glass-plus"></i>
                                Масштаб
                            </span>
                            <input
                                v-model.number="zoom"
                                type="range"
                                min="1"
                                max="3"
                                step="0.01"
                            />
                        </label>

                        <label class="profile-avatar-crop-control">
                            <span>
                                <i class="fas fa-arrows-left-right"></i>
                                Положение по горизонтали
                            </span>
                            <input
                                v-model.number="horizontalPosition"
                                type="range"
                                min="-100"
                                max="100"
                                step="1"
                            />
                        </label>

                        <label class="profile-avatar-crop-control">
                            <span>
                                <i class="fas fa-arrows-up-down"></i>
                                Положение по вертикали
                            </span>
                            <input
                                v-model.number="verticalPosition"
                                type="range"
                                min="-100"
                                max="100"
                                step="1"
                            />
                        </label>
                    </div>
                </div>

                <footer class="profile-avatar-crop-actions">
                    <button
                        class="profile-edit-secondary-btn"
                        type="button"
                        :disabled="isPreparing || isSubmitting"
                        @click="emit('cancel')"
                    >
                        Отмена
                    </button>
                    <button
                        class="profile-edit-main-btn"
                        type="button"
                        :disabled="isPreparing || isSubmitting"
                        @click="confirmCrop"
                    >
                        <i class="fas fa-check"></i>
                        {{ isPreparing || isSubmitting ? "Сохраняем..." : "Применить фото" }}
                    </button>
                </footer>
            </section>
        </div>
    </Teleport>
</template>
