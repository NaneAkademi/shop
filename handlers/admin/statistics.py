import inspect
from io import BytesIO

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import config
from callbacks import StatisticsCallback
from services.admin import AdminService
from utils.custom_filters import AdminIdFilter

statistics = Router()


async def statistics_menu(**kwargs):
    callback = kwargs.get("callback")
    state = kwargs.get("state")
    await state.clear()
    msg, kb_builder = await AdminService.get_statistics_menu()
    await callback.message.edit_text(text=msg, reply_markup=kb_builder.as_markup())


async def timedelta_picker(**kwargs):
    callback = kwargs.get("callback")
    msg, kb_builder = await AdminService.get_timedelta_menu(callback)
    await callback.message.edit_text(text=msg, reply_markup=kb_builder.as_markup())


async def entity_statistics(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await AdminService.get_statistics(callback, session)
    await callback.message.edit_text(text=msg, reply_markup=kb_builder.as_markup())


async def get_db_file(**kwargs):
    callback = kwargs.get("callback")
    await callback.answer()
    with open(f"./data/{config.DB_NAME}", "rb") as f:
        await callback.message.bot.send_document(callback.from_user.id,
                                                 types.BufferedInputFile(file=f.read(), filename="database.db"))


async def project_download(**kwargs):
    callback = kwargs.get("callback")
    await callback.answer()
    await callback.message.answer("🔄 Proje zip dosyası oluşturuluyor...")
    try:
        success_msg = await AdminService.create_project_zip(callback)
        if not success_msg.startswith("✅ Proje zip dosyası başarıyla"):
            await callback.message.answer(success_msg, parse_mode="HTML")
    except Exception as e:
        await callback.message.answer(f"❌ Zip dosyası oluşturulurken hata: {str(e)}")


@statistics.callback_query(AdminIdFilter(), StatisticsCallback.filter())
async def statistics_navigation(callback: CallbackQuery, state: FSMContext, callback_data: StatisticsCallback,
                                session: AsyncSession | Session):
    current_level = callback_data.level

    levels = {
        0: statistics_menu,
        1: timedelta_picker,
        2: entity_statistics,
        3: get_db_file,
        4: project_download
    }
    current_level_function = levels[current_level]

    kwargs = {
        "callback": callback,
        "state": state,
        "session": session,
    }

    await current_level_function(**kwargs)

    # Remove unused action matching since StatisticsCallback doesn't have action attribute
        