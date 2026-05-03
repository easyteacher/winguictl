# Security Notice

Important security considerations when using winguictl.

## Risk Description

winguictl directly controls your Windows desktop through simulated mouse clicks, keyboard input, and window operations. This tool can:

- Simulate mouse clicks and keyboard input
- Read window content through OCR and UIA
- Capture window screenshots
- Control window state (minimize, maximize, close)
- Type arbitrary text into any focused window

## Before Using winguictl

1. **Close sensitive applications** - Close or minimize windows containing passwords, personal messages, financial data, or other sensitive information
2. **Verify window IDs** - Always use exact `window_id` values from `window list` output
3. **Use dry-run mode** - Preview operations with `--dry-run` before execution
4. **Check screenshots** - Review captured screenshots before sharing

## Security Best Practices

### Window Targeting

- Use exact window IDs instead of fuzzy title matching
- Verify the window title matches your expectations before acting
- Use `snapshot` commands to inspect window structure

### Input Operations

- Use `--dry-run` to preview coordinates before clicking
- Be cautious with `type` commands that enter text
- Review OCR output before using coordinates

### Sensitive Data

- OCR captures all visible text, potentially including passwords or personal data
- Screenshots capture window content that may contain sensitive information
- Treat all captured data as untrusted

## Safety Boundaries

Use winguictl only for:

- Automating your own software
- Test environments
- Explicitly authorized systems

Do not use winguictl to:

- Bypass anti-bot checks or CAPTCHAs
- Automate unauthorized third-party systems
- Circumvent security controls

## See Also

For complete security guidelines, see [SECURITY.md](SECURITY.md).
