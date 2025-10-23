import { useEffect, useRef, useState } from "react";

// Card dimensions and styling
const CARD_WIDTH = 80;
const CARD_HEIGHT = 120;
const CARD_RADIUS = 8;
const CARD_LIFT_HEIGHT = 30;

// Suit colors and symbols
const SUIT_COLORS: Record<string, string> = {
  h: "#ef4444", // hearts - red
  d: "#3b82f6", // diamonds - blue
  s: "#1f2937", // spades - dark gray
  c: "#059669", // clubs - green
};

const SUIT_SYMBOLS: Record<string, string> = {
  h: "♥",
  d: "♦",
  s: "♠",
  c: "♣",
};

interface CardPosition {
  x: number;
  y: number;
  rotation: number;
  scale: number;
  opacity: number;
}

interface AnimatedCard {
  card: string;
  from: CardPosition;
  to: CardPosition;
  progress: number;
  duration: number;
  delay: number;
  onComplete?: () => void;
}

interface ParticleEffect {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
  size: number;
}

interface BotNotification {
  message: string;
  startTime: number;
  duration: number;
}

export interface GameCanvasProps {
  width?: number;
  height?: number;
  playerHand: string[];
  cardsOnBoard: Record<number, string | null>;
  prevTrick?: string[];
  activeSeat?: number;
  isMyTurn?: boolean;
  onCardClick?: (card: string) => void;
  hoveredCard?: string | null;
  selectedCards?: string[];
  currentPlayerName?: string;
  phase?: string;
  biddingWinnerSeat?: number | null;
  players: Array<{
    seat_number: number;
    screen_name: string;
    hand_size?: number;
    bot_strategy_kind?: string;
  }>;
}

export function GameCanvas({
  width = 1200,
  height = 800,
  playerHand = [],
  cardsOnBoard = {},
  prevTrick = [],
  activeSeat,
  isMyTurn,
  onCardClick,
  selectedCards = [],
  currentPlayerName = "You",
  phase = "",
  biddingWinnerSeat = null,
  players = [],
}: GameCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [animations, setAnimations] = useState<AnimatedCard[]>([]);
  const [particles, setParticles] = useState<ParticleEffect[]>([]);
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);
  const [botNotification, setBotNotification] = useState<BotNotification | null>(null);
  const animationFrameRef = useRef<number | undefined>(undefined);
  const lastTimeRef = useRef<number>(0);
  const lastActiveSeatRef = useRef<number | undefined>(undefined);

  // Show bot notification when active seat changes to a bot
  useEffect(() => {
    if (activeSeat && activeSeat !== lastActiveSeatRef.current) {
      const activePlayer = players.find(p => p.seat_number === activeSeat);
      if (activePlayer?.bot_strategy_kind) {
        setBotNotification({
          message: `${activePlayer.screen_name} is thinking...`,
          startTime: Date.now(),
          duration: 2000,
        });
      }
      lastActiveSeatRef.current = activeSeat;
    }
  }, [activeSeat, players]);

  // Calculate player positions in a circular layout
  // Current player is always at bottom, bots are distributed around the top
  const getPlayerPosition = (player: any) => {
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;

    // Find bots for positioning
    const bots = players.filter(p => p.bot_strategy_kind);
    
    // If this is the current player, position at bottom (already handled in hand rendering)
    if (!player.bot_strategy_kind) {
      return { x: centerX, y: height - 80 }; // Bottom position
    }
    
    // Position bots around the top of the table
    // If 2 bots: left and right. If 1 bot: top center
    const botIndex = bots.findIndex(b => b.seat_number === player.seat_number);
    const botCount = bots.length;
    
    if (botCount === 1) {
      // Single bot at top
      return { x: centerX, y: 100 };
    } else if (botCount === 2) {
      // Two bots: left and right
      if (botIndex === 0) {
        return { x: centerX - radius * 0.8, y: centerY - radius * 0.6 };
      } else {
        return { x: centerX + radius * 0.8, y: centerY - radius * 0.6 };
      }
    }
    
    // Fallback to circular layout
    const angle = Math.PI + (botIndex / botCount) * Math.PI;
    return {
      x: centerX + Math.cos(angle) * radius,
      y: centerY + Math.sin(angle) * radius,
    };
  };

  // Easing function for smooth animations
  const easeInOutCubic = (t: number): number => {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  };

  // Draw a single card
  const drawCard = (
    ctx: CanvasRenderingContext2D,
    card: string,
    x: number,
    y: number,
    rotation: number = 0,
    scale: number = 1,
    opacity: number = 1,
    isHovered: boolean = false,
    isSelected: boolean = false
  ) => {
    ctx.save();
    ctx.globalAlpha = opacity;

    // Apply transformations
    ctx.translate(x, y);
    ctx.rotate(rotation);
    ctx.scale(scale, scale);

    // Add glow effect for hovered or selected cards
    if (isHovered || isSelected) {
      ctx.shadowColor = isSelected ? "#a855f7" : "#3b82f6";
      ctx.shadowBlur = isSelected ? 25 : 20;
    }

    // Draw card background
    const suit = card.slice(-1);
    const rank = card.slice(0, -1);

    // Card background with gradient
    const gradient = ctx.createLinearGradient(
      -CARD_WIDTH / 2,
      -CARD_HEIGHT / 2,
      CARD_WIDTH / 2,
      CARD_HEIGHT / 2
    );
    gradient.addColorStop(0, "#ffffff");
    gradient.addColorStop(1, "#f3f4f6");

    ctx.fillStyle = gradient;
    ctx.strokeStyle = isSelected ? "#a855f7" : (isHovered ? "#3b82f6" : "#d1d5db");
    ctx.lineWidth = isSelected ? 4 : (isHovered ? 3 : 2);

    // Draw rounded rectangle
    ctx.beginPath();
    const cardX = -CARD_WIDTH / 2;
    const cardY = -CARD_HEIGHT / 2;
    const cardW = CARD_WIDTH;
    const cardH = CARD_HEIGHT;
    const cardR = CARD_RADIUS;
    
    ctx.moveTo(cardX + cardR, cardY);
    ctx.lineTo(cardX + cardW - cardR, cardY);
    ctx.quadraticCurveTo(cardX + cardW, cardY, cardX + cardW, cardY + cardR);
    ctx.lineTo(cardX + cardW, cardY + cardH - cardR);
    ctx.quadraticCurveTo(cardX + cardW, cardY + cardH, cardX + cardW - cardR, cardY + cardH);
    ctx.lineTo(cardX + cardR, cardY + cardH);
    ctx.quadraticCurveTo(cardX, cardY + cardH, cardX, cardY + cardH - cardR);
    ctx.lineTo(cardX, cardY + cardR);
    ctx.quadraticCurveTo(cardX, cardY, cardX + cardR, cardY);
    ctx.closePath();
    
    ctx.fill();
    ctx.stroke();

    // Draw rank
    ctx.fillStyle = SUIT_COLORS[suit] || "#000000";
    ctx.font = "bold 24px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(rank.toUpperCase(), 0, -CARD_HEIGHT / 4);

    // Draw suit symbol
    ctx.font = "36px sans-serif";
    ctx.fillText(SUIT_SYMBOLS[suit] || suit, 0, CARD_HEIGHT / 6);

    ctx.restore();
  };

  // Draw particles
  const drawParticle = (ctx: CanvasRenderingContext2D, particle: ParticleEffect) => {
    ctx.save();
    ctx.globalAlpha = particle.life / particle.maxLife;
    ctx.fillStyle = particle.color;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  };

  // Create particle burst effect
  const createParticleBurst = (x: number, y: number) => {
    const newParticles: ParticleEffect[] = [];
    for (let i = 0; i < 20; i++) {
      const angle = (Math.PI * 2 * i) / 20;
      const speed = 2 + Math.random() * 3;
      newParticles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 60,
        maxLife: 60,
        color: `hsl(${200 + Math.random() * 60}, 70%, 60%)`,
        size: 3 + Math.random() * 3,
      });
    }
    setParticles((prev) => [...prev, ...newParticles]);
  };

  // Animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const animate = (time: number) => {
      lastTimeRef.current = time;

      // Clear canvas
      ctx.clearRect(0, 0, width, height);

      // Draw background
      const bgGradient = ctx.createRadialGradient(
        width / 2,
        height / 2,
        0,
        width / 2,
        height / 2,
        Math.max(width, height) / 2
      );
      bgGradient.addColorStop(0, "#1e293b");
      bgGradient.addColorStop(1, "#0f172a");
      ctx.fillStyle = bgGradient;
      ctx.fillRect(0, 0, width, height);

      // Draw center table area
      ctx.save();
      ctx.fillStyle = "rgba(34, 197, 94, 0.2)";
      ctx.strokeStyle = "rgba(34, 197, 94, 0.4)";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, 200, 150, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      // Draw bot notification in center
      if (botNotification) {
        const elapsed = Date.now() - botNotification.startTime;
        if (elapsed < botNotification.duration) {
          const alpha = Math.min(1, 1 - elapsed / botNotification.duration);
          ctx.save();
          ctx.globalAlpha = alpha;
          ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
          ctx.strokeStyle = "#3b82f6";
          ctx.lineWidth = 2;
          const padding = 20;
          const textWidth = ctx.measureText(botNotification.message).width;
          const boxWidth = textWidth + padding * 2;
          const boxHeight = 40;
          const boxX = width / 2 - boxWidth / 2;
          const boxY = height / 2 - 100;
          
          ctx.beginPath();
          ctx.roundRect(boxX, boxY, boxWidth, boxHeight, 8);
          ctx.fill();
          ctx.stroke();
          
          ctx.fillStyle = "#ffffff";
          ctx.font = "16px sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(botNotification.message, width / 2, boxY + boxHeight / 2);
          ctx.restore();
        } else {
          setBotNotification(null);
        }
      }

      // Update and draw particles
      setParticles((prev) => {
        return prev
          .map((p) => ({
            ...p,
            x: p.x + p.vx,
            y: p.y + p.vy,
            vy: p.vy + 0.1, // gravity
            life: p.life - 1,
          }))
          .filter((p) => p.life > 0);
      });

      particles.forEach((particle) => drawParticle(ctx, particle));

      // Update animations
      setAnimations((prev) => {
        return prev
          .map((anim) => {
            const newProgress = Math.min(
              1,
              (time - anim.delay) / anim.duration / 1000
            );
            if (newProgress >= 1 && anim.onComplete) {
              anim.onComplete();
            }
            return { ...anim, progress: Math.max(0, newProgress) };
          })
          .filter((anim) => anim.progress < 1);
      });

      // Draw animated cards
      animations.forEach((anim) => {
        const t = easeInOutCubic(anim.progress);
        const x = anim.from.x + (anim.to.x - anim.from.x) * t;
        const y = anim.from.y + (anim.to.y - anim.from.y) * t;
        const rotation =
          anim.from.rotation + (anim.to.rotation - anim.from.rotation) * t;
        const scale = anim.from.scale + (anim.to.scale - anim.from.scale) * t;
        const opacity =
          anim.from.opacity + (anim.to.opacity - anim.from.opacity) * t;

        drawCard(ctx, anim.card, x, y, rotation, scale, opacity);
      });

      // Draw bot positions and labels (current player is at bottom with cards)
      players.forEach((player) => {
        // Skip current player - they're drawn at bottom with cards
        if (!player.bot_strategy_kind) return;
        
        const pos = getPlayerPosition(player);
        const isActive = activeSeat === player.seat_number;
        const isBiddingWinner = biddingWinnerSeat === player.seat_number;

        // Draw player indicator
        ctx.save();
        
        // Bidding winner gets golden highlight
        if (isBiddingWinner) {
          ctx.fillStyle = isActive ? "#f59e0b" : "#d97706";
          ctx.strokeStyle = "#fbbf24";
          ctx.lineWidth = 4;
          ctx.shadowColor = "#f59e0b";
          ctx.shadowBlur = 20;
        } else {
          ctx.fillStyle = isActive ? "#3b82f6" : "#4b5563";
          ctx.strokeStyle = isActive ? "#60a5fa" : "#6b7280";
          ctx.lineWidth = 3;
          if (isActive) {
            ctx.shadowColor = "#3b82f6";
            ctx.shadowBlur = 15;
          }
        }

        ctx.beginPath();
        ctx.arc(pos.x, pos.y, 30, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Draw player name
        ctx.shadowBlur = 0;
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 14px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(player.screen_name, pos.x, pos.y - 40);
        
        // Show "BIDDER" label for bidding winner
        if (isBiddingWinner) {
          ctx.fillStyle = "#fbbf24";
          ctx.font = "bold 10px sans-serif";
          ctx.fillText("BIDDER", pos.x, pos.y - 55);
        }

        // Draw card count
        if (player.hand_size) {
          ctx.fillStyle = "#9ca3af";
          ctx.font = "12px sans-serif";
          ctx.fillText(`${player.hand_size} cards`, pos.x, pos.y + 45);
        }

        ctx.restore();
      });

      // Draw cards on board - in a horizontal line with clear spacing
      const cardsOnBoardEntries = Object.entries(cardsOnBoard).filter(([, card]) => card);
      if (cardsOnBoardEntries.length > 0) {
        const centerX = width / 2;
        const centerY = height / 2 - 20; // Slightly above center for better visibility
        const cardSpacingOnBoard = 120; // Space between cards on board
        
        // Sort by seat number to ensure consistent ordering
        const sortedCards = cardsOnBoardEntries.sort(([a], [b]) => parseInt(a) - parseInt(b));
        
        // Calculate starting X position to center the cards
        const totalWidth = (sortedCards.length - 1) * cardSpacingOnBoard;
        const startX = centerX - totalWidth / 2;
        
        sortedCards.forEach(([seat, card], index) => {
          if (card) {
            const seatNum = parseInt(seat);
            const x = startX + index * cardSpacingOnBoard;
            const y = centerY;
            
            // Draw card with slight shadow for depth
            ctx.save();
            ctx.shadowColor = "rgba(0, 0, 0, 0.3)";
            ctx.shadowBlur = 10;
            ctx.shadowOffsetY = 5;
            drawCard(ctx, card, x, y, 0, 1.2, 1); // Slightly larger for visibility
            ctx.restore();
            
            // Draw player label below card
            const player = players.find(p => p.seat_number === seatNum);
            const isBidder = biddingWinnerSeat === seatNum;
            
            ctx.save();
            ctx.fillStyle = isBidder ? "#fbbf24" : "#9ca3af";
            ctx.font = "bold 12px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "top";
            ctx.fillText(
              player?.screen_name || `Seat ${seatNum}`,
              x,
              y + CARD_HEIGHT * 1.2 / 2 + 10
            );
            ctx.restore();
          }
        });
      }

      // Draw player hand at bottom with current player name
      const handY = height - 160; // Moved up to give space for action text below
      const handCenterX = width / 2;
      const cardSpacing = Math.min(100, (width - 200) / Math.max(playerHand.length, 1));

      // Draw current player name above hand
      ctx.save();
      const currentPlayerSeat = players.find(p => !p.bot_strategy_kind)?.seat_number;
      const isCurrentPlayerBidder = biddingWinnerSeat === currentPlayerSeat;
      
      if (isCurrentPlayerBidder) {
        ctx.fillStyle = "#f59e0b";
        ctx.shadowColor = "#f59e0b";
        ctx.shadowBlur = 15;
      } else {
        ctx.fillStyle = isMyTurn ? "#3b82f6" : "#9ca3af";
        if (isMyTurn) {
          ctx.shadowColor = "#3b82f6";
          ctx.shadowBlur = 10;
        }
      }
      
      ctx.font = "bold 18px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(currentPlayerName, handCenterX, handY - 70);
      
      // Show "BIDDER" label for current player if they won bid
      if (isCurrentPlayerBidder) {
        ctx.fillStyle = "#fbbf24";
        ctx.font = "bold 12px sans-serif";
        ctx.fillText("(BIDDER)", handCenterX, handY - 50);
      }
      
      // Draw phase info below name, above cards
      if (phase) {
        ctx.shadowBlur = 0;
        ctx.fillStyle = "#d1d5db";
        ctx.font = "12px sans-serif";
        ctx.fillText(phase, handCenterX, handY - 50);
      }
      ctx.restore();

      playerHand.forEach((card, index) => {
        const totalWidth = Math.max(0, (playerHand.length - 1) * cardSpacing);
        const x = handCenterX - totalWidth / 2 + index * cardSpacing;
        const isHovered = hoveredCard === card;
        const isSelected = selectedCards.includes(card);
        
        // Lift selected cards higher than hovered cards
        let y = handY;
        if (isSelected) {
          y = handY - CARD_LIFT_HEIGHT * 1.5;
        } else if (isHovered) {
          y = handY - CARD_LIFT_HEIGHT / 2;
        }
        
        const scale = isHovered && !isSelected ? 1.05 : 1;

        drawCard(ctx, card, x, y, 0, scale, 1, isHovered, isSelected);
      });

      // Draw previous trick in corner if exists
      if (prevTrick && prevTrick.length > 0) {
        ctx.save();
        ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
        ctx.fillRect(width - 250, 10, 240, 140);

        ctx.fillStyle = "#ffffff";
        ctx.font = "12px sans-serif";
        ctx.textAlign = "left";
        ctx.fillText("Previous Trick:", width - 240, 30);

        prevTrick.forEach((card, i) => {
          const x = width - 230 + (i % 4) * 55;
          const y = 60 + Math.floor(i / 4) * 70;
          drawCard(ctx, card, x, y, 0, 0.5, 0.8);
        });

        ctx.restore();
      }

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animationFrameRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [
    width,
    height,
    playerHand,
    cardsOnBoard,
    prevTrick,
    activeSeat,
    hoveredCard,
    selectedCards,
    currentPlayerName,
    phase,
    isMyTurn,
    players,
    animations,
    particles,
    botNotification,
  ]);

  // Handle card clicks
  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!onCardClick) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    // Account for canvas scaling
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    // Check if click is on player hand
    const handY = height - 160;
    const handCenterX = width / 2;
    const cardSpacing = Math.min(100, (width - 200) / Math.max(playerHand.length, 1));

    playerHand.forEach((card, index) => {
      const totalWidth = Math.max(0, (playerHand.length - 1) * cardSpacing);
      const cardX = handCenterX - totalWidth / 2 + index * cardSpacing;
      const isSelected = selectedCards.includes(card);
      const cardY = isSelected ? handY - CARD_LIFT_HEIGHT * 1.5 : handY;

      const dx = x - cardX;
      const dy = y - cardY;

      if (
        Math.abs(dx) < CARD_WIDTH / 2 &&
        Math.abs(dy) < CARD_HEIGHT / 2
      ) {
        onCardClick(card);
        
        // Create particle effect on click
        createParticleBurst(cardX, cardY);
      }
    });
  };

  // Handle mouse move for hover effect
  const handleCanvasMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    // Account for canvas scaling
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    // Check if hovering over player hand
    const handY = height - 160;
    const handCenterX = width / 2;
    const cardSpacing = Math.min(100, (width - 200) / Math.max(playerHand.length, 1));

    let newHoveredCard: string | null = null;

    playerHand.forEach((card, index) => {
      const totalWidth = Math.max(0, (playerHand.length - 1) * cardSpacing);
      const cardX = handCenterX - totalWidth / 2 + index * cardSpacing;
      const isSelected = selectedCards.includes(card);
      const cardY = isSelected ? handY - CARD_LIFT_HEIGHT * 1.5 : handY;

      const dx = x - cardX;
      const dy = y - cardY;

      if (
        Math.abs(dx) < CARD_WIDTH / 2 &&
        Math.abs(dy) < CARD_HEIGHT / 2
      ) {
        newHoveredCard = card;
      }
    });

    if (newHoveredCard !== hoveredCard) {
      setHoveredCard(newHoveredCard);
    }
  };

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      onClick={handleCanvasClick}
      onMouseMove={handleCanvasMouseMove}
      className="rounded-lg shadow-2xl cursor-pointer"
      style={{ maxWidth: "100%", height: "auto" }}
    />
  );
}
