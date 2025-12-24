declare module 'react-katex' {
    import { Component } from 'react';

    export interface MathComponentProps {
        math?: string;
        children?: string;
        errorColor?: string;
        renderError?: (error: Error | TypeError) => JSX.Element;
    }

    export class InlineMath extends Component<MathComponentProps> { }
    export class BlockMath extends Component<MathComponentProps> { }
}
