"use client";

interface SurveyFollowupStepProps {
  score: number;
  question: string;
  showQuoteConsent: boolean;
  answer: string;
  consentToQuote: boolean;
  error: string | null;
  sending: boolean;
  onAnswerChange: (value: string) => void;
  onConsentChange: (value: boolean) => void;
  onBack: () => void;
  onSkip: () => void;
  onSend: () => void;
}

export default function SurveyFollowupStep({
  score,
  question,
  showQuoteConsent,
  answer,
  consentToQuote,
  error,
  sending,
  onAnswerChange,
  onConsentChange,
  onBack,
  onSkip,
  onSend,
}: SurveyFollowupStepProps): React.ReactElement {
  return (
    <div>
      <p className="m-0 mb-3 text-[11px] font-medium text-EphapticOS-placeholder">Your score: {score}/10</p>

      <p className="m-0 mb-3.5 text-[13.5px] font-semibold text-EphapticOS-dark">{question}</p>

      <textarea
        value={answer}
        onChange={(e) => onAnswerChange(e.target.value)}
        placeholder="Optional, but it's the part we actually read."
        aria-label="Your answer"
        className="min-h-[78px] w-full resize-y rounded-lg border border-EphapticOS-border bg-EphapticOS-bg p-2.5 font-sans text-xs leading-relaxed text-EphapticOS-dark outline-none focus:border-EphapticOS-lavender"
      />

      {showQuoteConsent && (
        <label className="mt-3 flex items-center gap-2 text-xs text-EphapticOS-secondary">
          <input
            type="checkbox"
            checked={consentToQuote}
            onChange={(e) => onConsentChange(e.target.checked)}
            className="accent-EphapticOS-lavender"
          />
          OK to quote this publicly (first name only)?
        </label>
      )}

      {error && <p className="m-0 mt-2.5 text-xs text-red-500">{error}</p>}

      <div className="mt-4 flex items-center gap-2.5">
        <button type="button" onClick={onBack} className="mr-auto cursor-pointer bg-transparent p-0 text-xs text-EphapticOS-placeholder hover:text-EphapticOS-secondary">
          ← Back
        </button>
        <button
          type="button"
          onClick={onSkip}
          disabled={sending}
          className="cursor-pointer rounded-md border border-EphapticOS-border bg-transparent px-3.5 py-2 text-[13px] font-medium text-EphapticOS-secondary hover:text-EphapticOS-dark disabled:cursor-not-allowed disabled:opacity-45"
        >
          Skip
        </button>
        <button
          type="button"
          onClick={onSend}
          disabled={sending}
          className="cursor-pointer rounded-md bg-EphapticOS-lavender px-3.5 py-2 text-[13px] font-medium text-EphapticOS-lavender-text disabled:cursor-not-allowed disabled:opacity-45"
        >
          {sending ? "Sending…" : "Send"}
        </button>
      </div>
    </div>
  );
}
