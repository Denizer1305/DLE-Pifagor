<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

const props = defineProps<{
    variant: "forbidden" | "not-found";
}>();

const canvasRef = ref<HTMLCanvasElement | null>(null);
let animationFrame = 0;
let resizeHandler: (() => void) | null = null;

interface Particle {
    x: number;
    y: number;
    size: number;
    speedX: number;
    speedY: number;
    type: number;
}

function getParticleColors(): string[] {
    if (props.variant === "forbidden") {
        return ["#dc3545", "#4a6fa5", "#394458"];
    }

    return ["#4a6fa5", "#0fa0b3", "#394458"];
}

onMounted(() => {
    const canvasElement = canvasRef.value;

    if (!canvasElement) {
        return;
    }

    const drawingContext = canvasElement.getContext("2d");

    if (!drawingContext) {
        return;
    }

    const canvas = canvasElement;
    const context = drawingContext;
    let width = 0;
    let height = 0;
    let particles: Particle[] = [];

    function resize(): void {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        particles = Array.from({ length: 64 }, () => ({
            x: Math.random() * width,
            y: Math.random() * height,
            size: Math.random() * 2.4 + 0.8,
            speedX: Math.random() * 0.55 - 0.275,
            speedY: Math.random() * 0.55 - 0.275,
            type: Math.random(),
        }));
    }

    function draw(): void {
        const colors = getParticleColors();
        context.clearRect(0, 0, width, height);

        particles.forEach((particle, index) => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;

            if (particle.x > width) particle.x = 0;
            if (particle.x < 0) particle.x = width;
            if (particle.y > height) particle.y = 0;
            if (particle.y < 0) particle.y = height;

            context.globalAlpha = particle.type < 0.35 ? 0.34 : 0.18;
            context.fillStyle = colors[Math.min(colors.length - 1, Math.floor(particle.type * colors.length))] || colors[0] || "#4a6fa5";
            context.beginPath();
            context.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            context.fill();

            particles.slice(index + 1).forEach((nextParticle) => {
                const dx = particle.x - nextParticle.x;
                const dy = particle.y - nextParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 92) {
                    context.globalAlpha = 0.04;
                    context.strokeStyle = colors[0] || "#4a6fa5";
                    context.lineWidth = 0.5;
                    context.beginPath();
                    context.moveTo(particle.x, particle.y);
                    context.lineTo(nextParticle.x, nextParticle.y);
                    context.stroke();
                }
            });
        });

        animationFrame = window.requestAnimationFrame(draw);
    }

    resizeHandler = resize;
    resize();
    draw();
    window.addEventListener("resize", resize);
});

onBeforeUnmount(() => {
    window.cancelAnimationFrame(animationFrame);

    if (resizeHandler) {
        window.removeEventListener("resize", resizeHandler);
    }
});
</script>

<template>
    <div class="error-backdrop" aria-hidden="true">
        <canvas
            ref="canvasRef"
            class="error-backdrop__canvas"
        ></canvas>
        <span class="error-backdrop__shape error-backdrop__shape--one"></span>
        <span class="error-backdrop__shape error-backdrop__shape--two"></span>
        <span class="error-backdrop__shape error-backdrop__shape--three"></span>
    </div>
</template>
