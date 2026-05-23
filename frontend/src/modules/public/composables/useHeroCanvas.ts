import { onBeforeUnmount, onMounted, ref } from "vue";

interface Particle {
    x: number;
    y: number;
    vx: number;
    vy: number;
    radius: number;
    alpha: number;
}

const PARTICLE_COUNT = 58;
const LINK_DISTANCE = 130;

function createParticle(width: number, height: number): Particle {
    return {
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        radius: Math.random() * 1.8 + 0.8,
        alpha: Math.random() * 0.35 + 0.18,
    };
}

export function useHeroCanvas() {
    const heroCanvasRef = ref<HTMLCanvasElement | null>(null);

    let context: CanvasRenderingContext2D | null = null;
    let particles: Particle[] = [];
    let animationId = 0;

    function resizeCanvas(): void {
        const canvas = heroCanvasRef.value;

        if (!canvas) {
            return;
        }

        const rect = canvas.getBoundingClientRect();
        const ratio = window.devicePixelRatio || 1;

        canvas.width = Math.floor(rect.width * ratio);
        canvas.height = Math.floor(rect.height * ratio);
        canvas.style.width = `${rect.width}px`;
        canvas.style.height = `${rect.height}px`;

        context = canvas.getContext("2d");

        if (context) {
            context.setTransform(ratio, 0, 0, ratio, 0, 0);
        }

        particles = Array.from(
            {
                length: PARTICLE_COUNT,
            },
            () => createParticle(rect.width, rect.height),
        );
    }

    function draw(): void {
        const canvas = heroCanvasRef.value;

        if (!canvas || !context) {
            return;
        }

        const ctx = context;
        const rect = canvas.getBoundingClientRect();

        ctx.clearRect(0, 0, rect.width, rect.height);

        particles.forEach((particle, index) => {
            particle.x += particle.vx;
            particle.y += particle.vy;

            if (particle.x < 0 || particle.x > rect.width) {
                particle.vx *= -1;
            }

            if (particle.y < 0 || particle.y > rect.height) {
                particle.vy *= -1;
            }

            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(74, 111, 165, ${particle.alpha})`;
            ctx.fill();

            for (let nextIndex = index + 1; nextIndex < particles.length; nextIndex += 1) {
                const nextParticle = particles[nextIndex];

                if (!nextParticle) {
                    continue;
                }

                const distance = Math.hypot(
                    particle.x - nextParticle.x,
                    particle.y - nextParticle.y,
                );

                if (distance < LINK_DISTANCE) {
                    const opacity = (1 - distance / LINK_DISTANCE) * 0.12;

                    ctx.beginPath();
                    ctx.moveTo(particle.x, particle.y);
                    ctx.lineTo(nextParticle.x, nextParticle.y);
                    ctx.strokeStyle = `rgba(74, 111, 165, ${opacity})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
        });

        animationId = window.requestAnimationFrame(draw);
    }

    function start(): void {
        resizeCanvas();
        draw();

        window.addEventListener("resize", resizeCanvas);
    }

    function stop(): void {
        window.cancelAnimationFrame(animationId);
        window.removeEventListener("resize", resizeCanvas);
    }

    onMounted(() => {
        start();
    });

    onBeforeUnmount(() => {
        stop();
    });

    return {
        heroCanvasRef,
    };
}
