import React from 'react';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

interface MathTextProps {
    text: string;
    className?: string;
}

/**
 * Component to render text with LaTeX math expressions
 * Supports inline math: $...$ or \(...\)
 * Supports block math: $$...$$ or \[...\]
 */
export function MathText({ text, className = '' }: MathTextProps) {
    if (!text) return null;

    // First, normalize LaTeX delimiters and commands
    let normalizedText = text
        // Convert \( \) to $ $ and \[ \] to $$ $$
        .replace(/\\\(/g, '$')
        .replace(/\\\)/g, '$')
        .replace(/\\\[/g, '$$')
        .replace(/\\\]/g, '$$')
        // Handle escaped underscores (convert \_ to _)
        .replace(/\\_/g, '_')
        // Handle \textbf{text} - convert to bold markdown or just remove for now
        .replace(/\\textbf\{([^}]+)\}/g, '**$1**');

    // Split text by LaTeX delimiters
    const parts: React.ReactElement[] = [];
    let currentIndex = 0;
    let key = 0;

    // Match both inline $...$ and block $$...$$ math
    const regex = /\$\$([^$]+)\$\$|\$([^$]+)\$/g;
    let match;

    while ((match = regex.exec(normalizedText)) !== null) {
        // Add text before the math
        if (match.index > currentIndex) {
            parts.push(
                <span key={`text-${key++}`}>
                    {normalizedText.substring(currentIndex, match.index)}
                </span>
            );
        }

        // Add the math expression
        if (match[1]) {
            // Block math $$...$$
            parts.push(
                <BlockMath key={`math-${key++}`} math={match[1]} />
            );
        } else if (match[2]) {
            // Inline math $...$
            parts.push(
                <InlineMath key={`math-${key++}`} math={match[2]} />
            );
        }

        currentIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (currentIndex < normalizedText.length) {
        parts.push(
            <span key={`text-${key++}`}>
                {normalizedText.substring(currentIndex)}
            </span>
        );
    }

    return <span className={`inline ${className}`} style={{ display: 'inline' }}>{parts}</span>;
}

