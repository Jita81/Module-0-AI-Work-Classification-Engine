# AI Work Classification Engine Configuration

This directory contains configuration files for the AI Work Classification Engine.

## Files

- `prompts.json` - Claude API prompts and system messages
- `standards.json` - Classification standards for Size, Complexity, and Type
- `versions/` - Version history of configuration changes

## Standards Overview

### Size Standards
- **XS**: < 1 day (Trivial changes)
- **S**: 1-3 days (Small, well-defined changes)
- **M**: 1-2 weeks (Medium-sized features)
- **L**: 2-4 weeks (Large features)
- **XL**: 1-2 months (Major features)
- **XXL**: 2+ months (Enterprise-level initiatives)

### Complexity Standards
- **Low**: Well-understood work with established patterns
- **Medium**: Some unknowns with moderate integration
- **High**: Significant unknowns requiring research
- **Critical**: Mission-critical with extensive dependencies

### Type Standards
- **Feature**: New functionality or capabilities
- **Enhancement**: Improvements to existing functionality
- **Bug**: Defect fixes and corrections
- **Infrastructure**: Platform, tooling, or system improvements
- **Migration**: Moving or upgrading systems/data
- **Research**: Investigation, proof of concepts, spikes
- **Epic**: Large initiative containing multiple features

## Configuration Updates

The system automatically learns from user feedback and can update these standards. All changes are versioned and can be rolled back if needed.

## Usage

These configuration files are loaded by the AI Work Classification Engine at startup and can be modified through the web interface or API endpoints.
