import difflib, yaml, sys, json
from pathlib import Path
from .ingestion import openapi_loader
from .telemetry import log_event
def diff_and_propose(old_spec, new_spec):
    old=openapi_loader.load(old_spec); new=openapi_loader.load(new_spec)
    os=(old.get('components') or {}).get('schemas',{}); ns=(new.get('components') or {}).get('schemas',{})
    props=lambda x:(x or {}).get('properties') or {}
    ren=[]; stat=[]
    for name, ov in os.items():
        nv=ns.get(name,{})
        for op in props(ov).keys():
            best,score=None,0.0
            for np in props(nv).keys():
                r=difflib.SequenceMatcher(None, op.lower(), np.lower()).ratio()
                if r>score: best,score=np,r
            if best and best!=op and score>=0.75: ren.append({'schema':name,'from':op,'to':best,'confidence':round(score,2)})
    for path,item in (new.get('paths') or {}).items():
        for m,op in (item or {}).items():
            nres=set(str(k) for k in (op.get('responses') or {}).keys())
            ores=set(str(k) for k in ((old.get('paths') or {}).get(path,{}).get(m,{}).get('responses') or {}).keys())
            add=list(nres-ores)
            if add: stat.append({'path':path,'method':m.upper(),'added':add})
    log_event({'type':'heal_proposed','summary':str({'field_renames':ren,'status_changes':stat})})
    return {'field_renames':ren,'status_changes':stat}

def display_proposed_heals(props):
    """Display proposed healing changes for human review"""
    print("\n🔍 PROPOSED HEALING CHANGES")
    print("=" * 50)

    field_renames = props.get('field_renames', [])
    status_changes = props.get('status_changes', [])

    if field_renames:
        print(f"\n📝 Field Renames ({len(field_renames)} proposed):")
        print("-" * 40)
        for i, rename in enumerate(field_renames, 1):
            confidence_pct = f"{rename['confidence']*100:.1f}%"
            print(f"{i}. Schema: {rename['schema']}")
            print(f"   From: '{rename['from']}' → To: '{rename['to']}'")
            print(f"   Confidence: {confidence_pct}")
            print()

    if status_changes:
        print(f"\n🔄 Status Code Changes ({len(status_changes)} proposed):")
        print("-" * 40)
        for i, change in enumerate(status_changes, 1):
            print(f"{i}. {change['method']} {change['path']}")
            print(f"   Added status codes: {', '.join(change['added'])}")
            print()

    if not field_renames and not status_changes:
        print("\n✅ No healing changes proposed - APIs are compatible!")
        return

def get_user_approval(props, confidence_threshold=0.6):
    """Interactive human approval process for healing changes"""
    field_renames = props.get('field_renames', [])
    status_changes = props.get('status_changes', [])

    if not field_renames and not status_changes:
        print("✅ No healing changes needed.")
        return []

    # Filter by confidence threshold
    high_confidence_renames = [p for p in field_renames if p['confidence'] >= confidence_threshold]
    low_confidence_renames = [p for p in field_renames if p['confidence'] < confidence_threshold]

    approved_changes = []

    # Handle high confidence renames
    if high_confidence_renames:
        print(f"\n🟢 HIGH CONFIDENCE CHANGES (≥{confidence_threshold*100:.0f}% confidence):")
        for rename in high_confidence_renames:
            confidence_pct = f"{rename['confidence']*100:.1f}%"
            response = input(f"Apply rename '{rename['from']}' → '{rename['to']}' ({confidence_pct})? [Y/n]: ").strip().lower()
            if response in ('', 'y', 'yes'):
                approved_changes.append(rename)
                print("  ✅ Approved")
            else:
                print("  ❌ Rejected")

    # Handle low confidence renames
    if low_confidence_renames:
        print(f"\n🟡 LOW CONFIDENCE CHANGES (<{confidence_threshold*100:.0f}% confidence):")
        for rename in low_confidence_renames:
            confidence_pct = f"{rename['confidence']*100:.1f}%"
            response = input(f"Apply rename '{rename['from']}' → '{rename['to']}' ({confidence_pct})? [y/N]: ").strip().lower()
            if response in ('y', 'yes'):
                approved_changes.append(rename)
                print("  ✅ Approved")
            else:
                print("  ❌ Rejected")

    # Handle status changes
    if status_changes:
        print(f"\n🔄 STATUS CODE CHANGES:")
        for change in status_changes:
            codes_str = ', '.join(change['added'])
            response = input(f"Add status codes [{codes_str}] to {change['method']} {change['path']}? [Y/n]: ").strip().lower()
            if response in ('', 'y', 'yes'):
                approved_changes.append(change)
                print("  ✅ Approved")
            else:
                print("  ❌ Rejected")

    return approved_changes

def apply_heals(props, confidence_threshold=0.6, interactive=False, auto_apply=False):
    """
    Apply healing changes with optional human oversight

    Args:
        props: Proposed healing changes
        confidence_threshold: Minimum confidence for auto-approval
        interactive: Enable interactive human review
        auto_apply: Skip human approval entirely
    """
    field_renames = props.get('field_renames', [])
    status_changes = props.get('status_changes', [])

    if not field_renames and not status_changes:
        print("✅ No healing changes needed.")
        log_event({'type':'heal_completed', 'summary':'No changes needed'})
        return []

    # Display proposed changes
    display_proposed_heals(props)

    approved_changes = []

    if interactive:
        # Interactive human approval
        print("\n🤝 HUMAN OVERSIGHT MODE")
        print("Please review each proposed change:")
        approved_changes = get_user_approval(props, confidence_threshold)
    elif auto_apply:
        # Auto-apply all changes above threshold
        approved_changes = [p for p in field_renames if p['confidence'] >= confidence_threshold]
        print(f"\n🤖 AUTO-APPLYING {len(approved_changes)} high-confidence changes...")
    else:
        # Default: filter by confidence but require explicit approval
        high_confidence = [p for p in field_renames if p['confidence'] >= confidence_threshold]
        if high_confidence:
            print(f"\n⚠️  {len(high_confidence)} changes ready for application (confidence ≥{confidence_threshold*100:.0f}%)")
            response = input("Apply these changes? [Y/n]: ").strip().lower()
            if response in ('', 'y', 'yes'):
                approved_changes = high_confidence
                print("  ✅ Approved for application")
            else:
                print("  ❌ Changes not applied")
        else:
            print(f"\n⚠️  No changes meet the confidence threshold (≥{confidence_threshold*100:.0f}%)")

    # Apply approved changes
    if approved_changes:
        # Save only field renames (status changes are informational)
        renames_only = [p for p in approved_changes if 'from' in p and 'to' in p]
        patches_file = Path('healer_patches.yaml')
        existing_patches = {}

        if patches_file.exists():
            with open(patches_file, 'r', encoding='utf-8') as f:
                existing_patches = yaml.safe_load(f) or {}

        existing_renames = existing_patches.get('renames', [])
        all_renames = existing_renames + renames_only

        with open(patches_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump({'renames': all_renames}, f)

        log_event({
            'type':'heal_applied',
            'summary': f'{len(renames_only)} renames approved and applied',
            'details': {
                'approved_count': len(approved_changes),
                'applied_renames': len(renames_only),
                'interactive_mode': interactive,
                'auto_mode': auto_apply
            }
        })

        print(f"\n✅ Applied {len(renames_only)} healing patches to healer_patches.yaml")
        return renames_only
    else:
        log_event({'type':'heal_cancelled', 'summary':'No changes approved by user'})
        print("\n❌ No changes applied.")
        return []
