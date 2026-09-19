from django.core.management.base import BaseCommand
from tracker.models import Article, DailyQuote


ARTICLES = [
    {
        "title": "5 Ways to Be Dangerously Charismatic",
        "slug": "5-ways-dangerously-charismatic",
        "category": "mental",
        "excerpt": "Charisma isn't born — it's built. Here are five subtle shifts that make people lean in.",
        "body": "1. Master the pause. Silence is magnetic.\n2. Use their name softly.\n3. Listen to understand, not to reply.\n4. Let your presence be calm, not loud.\n5. Praise specifically, never generically.",
    },
    {
        "title": "5 Lessons Every First Child Should Learn",
        "slug": "5-lessons-first-child",
        "category": "mental",
        "excerpt": "Being the eldest is a role, not a life sentence.",
        "body": "1. You are allowed to be taken care of.\n2. Your worth isn't your responsibility.\n3. Boundaries are love, not betrayal.\n4. Rest is productive.\n5. You get to rewrite the family story.",
    },
    {
        "title": "5 Things to Remember While Growing and Healing",
        "slug": "5-things-growing-healing",
        "category": "mental",
        "excerpt": "Healing isn't linear — and that's the point.",
        "body": "1. Progress hides in quiet days.\n2. Triggers are information, not failure.\n3. Your pace is your own.\n4. Community heals what isolation broke.\n5. You are becoming, not broken.",
    },
    {
        "title": "Uncomfortable Questions You Must Ask Yourself",
        "slug": "uncomfortable-questions",
        "category": "mental",
        "excerpt": "The answers will change your next decade.",
        "body": "• What am I pretending not to know?\n• Where am I shrinking to be liked?\n• What would I do if I trusted myself fully?\n• Whose approval am I still chasing?\n• What does my body need that my mind keeps ignoring?",
    },
    {
        "title": "The 7-Minute Glow Routine",
        "slug": "7-minute-glow-routine",
        "category": "physical",
        "excerpt": "Radiance isn't complicated — it's consistent.",
        "body": "1. Cold rinse for circulation.\n2. Gua sha for lymphatic flow.\n3. SPF — always.\n4. Hydration from inside out.\n5. Posture reset: crown to ceiling.\n6. Three deep breaths before your mirror.\n7. Speak one kind thing to yourself.",
    },
    {
        "title": "Financial Freedom Is Self-Care",
        "slug": "financial-freedom-self-care",
        "category": "financial",
        "excerpt": "Your bank account is a mirror of your boundaries.",
        "body": "Start with the 50/30/20 rule. Track for 30 days. Don't judge — just observe. Then adjust. Money isn't masculine or feminine — it's neutral, and it responds to attention.",
    },
]

QUOTES = [
    "5 ways to upgrade your life in silence.",
    "You are allowed to outgrow people who no longer fit.",
    "Softness is a strategy, not a weakness.",
    "Discipline is the highest form of self-love.",
    "Bloom quietly. Let the results speak.",
    "Your peace is not up for negotiation.",
    "Boundaries are the language of self-respect.",
]


class Command(BaseCommand):
    help = 'Seed initial articles and quotes'

    def handle(self, *args, **kwargs):
        for a in ARTICLES:
            Article.objects.get_or_create(slug=a['slug'], defaults=a)
        for q in QUOTES:
            DailyQuote.objects.get_or_create(text=q)
        self.stdout.write(self.style.SUCCESS('Seeded successfully.'))